"""Bộ máy gợi ý đề tài — mô hình kết hợp (ensemble) hai giai đoạn.

Giai đoạn 1: lọc cứng (GPA sàn, môn tiên quyết, kỹ năng bắt buộc) → tính M1–M4 cho mọi đề tài đủ điều kiện → lấy Top-K.
Giai đoạn 2: LLM chấm M5 cho Top-K → điểm cuối = tổng có trọng số → Top 5.

Mỗi mô hình trả về điểm 0–100. Công thức xem docs/KE-HOACH (mục 6).
"""

from dataclasses import dataclass, field

from django.conf import settings

from catalog.models import Student, Topic
from recommend.llm import batch_score_llm, score_pair

__all__ = [
    "DEFAULT_WEIGHTS",
    "WEIGHTS_VERSION",
    "Candidate",
    "Profile",
    "SemanticModel",
    "eligible",
    "explain",
    "m1_skill",
    "m2_academic",
    "m3_field",
    "m4_semantic",
    "score_pair",
    "score_student",
]

# Trọng số w1..w5 (kỹ năng, học lực, lĩnh vực, ngữ nghĩa, LLM). Bản chính thức sẽ lấy từ AHP do GVHD so sánh cặp.
DEFAULT_WEIGHTS = {"skill": 0.25, "academic": 0.20, "field": 0.15, "semantic": 0.20, "llm": 0.20}
WEIGHTS_VERSION = "expert-v0"


def get_active_weights():
    """Lấy bộ trọng số đang dùng (is_active=True) từ CSDL. Nếu không có → DEFAULT_WEIGHTS."""
    try:
        from recommend.models import WeightSet

        active = WeightSet.objects.filter(is_active=True).first()
        if active and active.weights:
            return active.weights
    except Exception:
        pass
    return DEFAULT_WEIGHTS


def get_active_weights_version():
    """Lấy tên phiên bản bộ trọng số đang dùng từ CSDL. Nếu không có → WEIGHTS_VERSION."""
    try:
        from recommend.models import WeightSet

        active = WeightSet.objects.filter(is_active=True).first()
        if active and active.name:
            return active.name
    except Exception:
        pass
    return WEIGHTS_VERSION


@dataclass
class Candidate:
    topic: Topic
    scores: dict = field(default_factory=dict)  # skill, academic, field, semantic, llm → 0..100 (None = chưa có)
    reasons: list = field(default_factory=list)
    llm_reason: str = ""

    def final(self, weights):
        """Tổng có trọng số; thành phần chưa có (None) bị bỏ và chia lại trọng số các thành phần còn lại."""
        have = {k: v for k, v in self.scores.items() if v is not None}
        total_w = sum(weights[k] for k in have)
        return sum(weights[k] * v for k, v in have.items()) / total_w if total_w else 0.0


# ---------------------------------------------------------------- dữ liệu sinh viên gom sẵn (đỡ truy vấn lặp)
class Profile:
    def __init__(self, student: Student):
        self.student = student
        self.gpa = float(student.gpa)
        self.skills = {s.skill_id: s.level for s in student.skills.all()}
        self.interests = {i.field_id: i.level for i in student.interests.all()}
        self.courses = {r.course_id: float(r.score) for r in student.course_results.select_related("course")}
        self.course_fields = {r.course_id: r.course.field_id for r in student.course_results.select_related("course")}


# ---------------------------------------------------------------- lọc cứng (BR1)
def eligible(p: Profile, topic: Topic):
    """Trả về (đủ điều kiện?, lý do nếu không)."""
    if p.gpa < float(topic.min_gpa):
        return False, f"GPA {p.gpa} thấp hơn yêu cầu {topic.min_gpa}"
    for pre in topic.prerequisites.all():
        if p.courses.get(pre.course_id, 0) < float(pre.min_score):
            return False, f"Chưa đạt môn tiên quyết {pre.course.name}"
    for ts in topic.skills.all():
        if ts.is_mandatory and p.skills.get(ts.skill_id, 0) < ts.required_level:
            return False, f"Chưa đạt kỹ năng bắt buộc {ts.skill.name} (cần mức {ts.required_level})"
    return True, ""


def eligibility_reasons(p: Profile, topic: Topic):
    """Từng điều kiện bắt buộc của đề tài với giá trị yêu cầu / thực tế của SV — để giao diện nói rõ thiếu gì.

    Cùng luật với eligible() (GPA, môn tiên quyết, kỹ năng bắt buộc); đề tài đủ điều kiện ⇔ mọi mục ok=True.
    """
    out = [
        {
            "rule_type": "gpa",
            "label": "GPA tối thiểu",
            "required": float(topic.min_gpa),
            "actual": p.gpa,
            "ok": p.gpa >= float(topic.min_gpa),
        }
    ]
    for pre in topic.prerequisites.all():
        have = p.courses.get(pre.course_id)
        out.append(
            {
                "rule_type": "course",
                "label": f"Môn {pre.course.name}",
                "required": float(pre.min_score),
                "actual": have,
                "ok": (have or 0) >= float(pre.min_score),
            }
        )
    for ts in topic.skills.all():
        if ts.is_mandatory:
            have = p.skills.get(ts.skill_id, 0)
            out.append(
                {
                    "rule_type": "skill",
                    "label": f"Kỹ năng {ts.skill.name}",
                    "required": ts.required_level,
                    "actual": have,
                    "ok": have >= ts.required_level,
                }
            )
    return out


# ---------------------------------------------------------------- M1: khớp kỹ năng
def m1_skill(p: Profile, topic: Topic):
    """M1 = 100 · Σ w_k·min(mức_SV/mức_yêu_cầu, 1) / Σ w_k  — đáp ứng bao nhiêu phần kỹ năng đề tài cần."""
    req = list(topic.skills.all())
    if not req:
        return 100.0, []
    num = sum(ts.weight * min(p.skills.get(ts.skill_id, 0) / ts.required_level, 1) for ts in req)
    missing = [ts.skill.name for ts in req if p.skills.get(ts.skill_id, 0) < ts.required_level]
    return 100 * num / sum(ts.weight for ts in req), missing


# ---------------------------------------------------------------- M2: học lực
def m2_academic(p: Profile, topic: Topic):
    """M2 = 100 · (0,4·GPA/4 + 0,6·điểm TB các môn liên quan/10).
    Môn liên quan = môn tiên quyết + môn cùng lĩnh vực đề tài.
    Thang cố định theo quy chế (không chuẩn hoá theo dữ liệu) để điểm không đổi khi thêm sinh viên."""
    topic_fields = {f.id for f in topic.fields.all()}
    related = {pre.course_id for pre in topic.prerequisites.all()} | {
        c for c, f in p.course_fields.items() if f in topic_fields
    }
    scores = [p.courses[c] for c in related if c in p.courses]
    avg = sum(scores) / len(scores) if scores else p.gpa * 2.5  # không có môn liên quan → quy đổi từ GPA
    return 100 * (0.4 * p.gpa / 4 + 0.6 * avg / 10)


# ---------------------------------------------------------------- M3: khớp lĩnh vực quan tâm
def m3_field(p: Profile, topic: Topic):
    """M3 = 100 · trung bình trên các lĩnh vực của đề tài của (mức quan tâm của SV / 3).
    Đề tài thuộc lĩnh vực nào thì xem SV quan tâm lĩnh vực đó đến đâu. (Bản Jaccard trước đó trừ điểm SV quan tâm
    nhiều lĩnh vực: đề tài IoT chỉ được 33 dù SV quan tâm IoT tối đa — đã thay ngày 02/10.)"""
    topic_fields = [f.id for f in topic.fields.all()]
    if not topic_fields:
        return 0.0
    return 100 * sum(p.interests.get(f, 0) / 3 for f in topic_fields) / len(topic_fields)


# ---------------------------------------------------------------- M4: độ gần nghĩa (embedding)
class SemanticModel:
    """Mô hình ngôn ngữ biến câu thành vector 384 chiều; hai câu càng gần nghĩa thì cosine càng lớn.
    Tải một lần (khoảng 470 MB, chạy CPU). Vector đề tài được nhớ theo (id, version)
    nên chỉ tính lại khi GV sửa đề tài."""

    NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    _model = None
    _topic_vecs = {}

    @classmethod
    def model(cls):
        if cls._model is None:
            from sentence_transformers import (
                SentenceTransformer,  # import muộn: các phần khác không phải chờ tải mô hình
            )

            cls._model = SentenceTransformer(cls.NAME)
        return cls._model

    @classmethod
    def encode(cls, texts):
        return cls.model().encode(list(texts), normalize_embeddings=True, show_progress_bar=False)

    @classmethod
    def topic_vectors(cls, topics):
        todo = [t for t in topics if (t.id, t.version) not in cls._topic_vecs]
        if todo:
            for t, v in zip(todo, cls.encode(f"{t.title}. {t.description}" for t in todo), strict=True):
                cls._topic_vecs[(t.id, t.version)] = v
        return [cls._topic_vecs[(t.id, t.version)] for t in topics]


def m4_semantic(student_vec, topic_vec):
    """M4 = 100 · max(0, cos(e_SV, e_đềtài)). Vector đã chuẩn hoá độ dài 1 nên cosine = tích vô hướng."""
    return 100 * max(0.0, float(student_vec @ topic_vec))


# ---------------------------------------------------------------- ghép lại
def compute_stage1_candidates(
    student: Student,
    topics=None,
    weights=None,
    top_k: int = 15,
    semantic: bool = True,
) -> list[Candidate]:
    """Giai đoạn 1: Lọc cứng (BR1) và tính điểm M1-M4 để chọn ra Top-K ứng viên (mặc định 15 đề tài).
    - M1: Khớp kỹ năng (0..100)
    - M2: Học lực và môn liên quan (0..100)
    - M3: Khớp lĩnh vực quan tâm (0..100)
    - M4: Độ gần nghĩa ngữ nghĩa qua embedding MiniLM (0..100, nếu semantic=True)
    """
    weights = weights or get_active_weights()
    p = Profile(student)
    topics = (
        topics
        if topics is not None
        else Topic.objects.filter(status=Topic.Status.OPEN).prefetch_related(
            "skills__skill", "prerequisites__course", "fields"
        )
    )
    out = []
    for t in topics:
        ok, _ = eligible(p, t)
        if not ok:
            continue
        s1, missing = m1_skill(p, t)
        c = Candidate(
            t, {"skill": s1, "academic": m2_academic(p, t), "field": m3_field(p, t), "semantic": None, "llm": None}
        )
        if missing:
            c.reasons.append("Cần bổ sung: " + ", ".join(missing))
        out.append(c)
    if semantic and out and student.about.strip():
        sv = SemanticModel.encode([student.about])[0]
        for c, tv in zip(out, SemanticModel.topic_vectors([c.topic for c in out]), strict=True):
            c.scores["semantic"] = m4_semantic(sv, tv)
    out.sort(key=lambda c: c.final(weights), reverse=True)
    return out[:top_k]


def apply_stage2_llm(student: Student, cands: list[Candidate], weights: dict) -> list[Candidate]:
    """Giai đoạn 2: Gọi LLM chấm M5 theo rubric 100 điểm cho Top-K ứng viên:
    - Trộn ngẫu nhiên thứ tự đề tài trước khi gửi, ghép lại theo topic_id.
    - Kiểm tra tổng rubric: total = feasibility + career + nature + motivation (0..100).
      Nếu sai thì bỏ điểm M5 của đề tài đó (m5=None), đề tài vẫn được xếp hạng bằng M1–M4.
    - Lỗi mạng/JSON sau 1 lần thử lại → m5=None (Candidate.final tự chia lại trọng số).
    - Xếp hạng lại theo điểm cuối có trọng số w1..w5.
    """
    # điểm LLM sai rubric chỉ bỏ M5 của đề tài đó (Candidate.final chia lại trọng số), KHÔNG loại đề tài
    scored_dict, _invalid = batch_score_llm(student, [c.topic for c in cands])

    for c in cands:
        if c.topic.id in scored_dict:
            res = scored_dict[c.topic.id]
            c.scores["llm"] = float(res.total)
            c.llm_reason = res.reason

    cands.sort(key=lambda c: c.final(weights), reverse=True)
    return cands


def score_student(
    student: Student,
    topics=None,
    weights=None,
    top_k: int = 15,
    semantic: bool = True,
    llm: bool | None = None,
) -> list[Candidate]:
    """Giai đoạn 1 + Giai đoạn 2 cho một sinh viên:
    1. Giai đoạn 1: lọc cứng + M1-M4 → lấy Top-K ứng viên (mặc định 15).
    2. Giai đoạn 2: LLM chấm M5 theo rubric 100 điểm cho Top-K → tính điểm cuối có trọng số → xếp hạng lại.
    - semantic=False: bỏ M4 (dùng cho thực nghiệm ablation và kiểm thử nhanh).
    - llm=False: bỏ M5 (hoặc tắt qua settings RECOMMEND_LLM=0).
    """
    weights = weights or get_active_weights()
    cands = compute_stage1_candidates(student, topics, weights, top_k, semantic)
    should_run_llm = getattr(settings, "RECOMMEND_LLM", True) if llm is None else llm
    if should_run_llm and cands:
        cands = apply_stage2_llm(student, cands, weights)
    return cands


def explain_heuristic(c: Candidate) -> str:
    """Lời giải thích bằng mẫu câu từ điểm thành phần (dùng khi chưa có/không có LLM)."""
    s = c.scores
    parts = []
    if s["skill"] >= 80:
        parts.append("bạn đáp ứng tốt các kỹ năng đề tài cần")
    elif s["skill"] >= 50:
        parts.append("bạn đáp ứng một phần kỹ năng đề tài cần")
    if s["field"] >= 50:
        parts.append("đề tài thuộc lĩnh vực bạn quan tâm")
    if (s.get("semantic") or 0) >= 35:
        parts.append("mô tả đề tài gần với định hướng bạn tự giới thiệu")
    if s["academic"] >= 70:
        parts.append("kết quả các môn liên quan của bạn tốt")
    text = ("Phù hợp vì " + ", ".join(parts) + ".") if parts else "Mức phù hợp trung bình."
    return " ".join([text] + c.reasons)


def explain(c: Candidate) -> str:
    """Lời giải thích hiển thị cho đề tài gợi ý:
    - Dùng lý do (reason) của LLM nếu có, nối với 'Cần bổ sung: …' từ M1.
    - Nếu không có LLM: giải thích bằng mẫu câu heurictic từ M1-M4.
    """
    missing = [r for r in c.reasons if r.startswith("Cần bổ sung:")]
    missing_str = " ".join(missing)
    if c.llm_reason:
        return f"{c.llm_reason} {missing_str}".strip() if missing_str else c.llm_reason.strip()
    return explain_heuristic(c)
