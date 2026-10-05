"""Mô-đun LLM chấm điểm theo rubric 100 điểm (Giai đoạn 2 của gợi ý).

Rubric đánh giá M5 (100 điểm, KHÔNG chấm lại kỹ năng/GPA):
- feasibility: khả thi theo kinh nghiệm tự kể của sinh viên (0..35 điểm)
- career: gắn với định hướng nghề nghiệp của sinh viên (0..30 điểm)
- nature: tính chất đề tài ứng dụng hoặc nghiên cứu (0..20 điểm)
- motivation: động lực thể hiện trong giới thiệu bản thân (0..15 điểm)
Công thức: total = feasibility + career + nature + motivation (0..100).
"""

import hashlib
import json
import logging
import random
import urllib.error
import urllib.request
from typing import Any

from django.conf import settings

from catalog.models import Student, Topic
from recommend.models import LLMScore

logger = logging.getLogger(__name__)

PROMPT_VERSION = "v1"

SYSTEM_PROMPT = (
    "Bạn là trợ lý AI đánh giá mức độ phù hợp của đề tài tốt nghiệp cho sinh viên theo rubric 100 điểm.\n"
    "QUY TẮC BẮT BUỘC:\n"
    "1. KHÔNG chấm lại kỹ năng và GPA (hệ thống đã tính ở giai đoạn 1).\n"
    "2. Chỉ dùng dữ liệu được cung cấp, thiếu coi là không có, không tự suy đoán.\n"
    "3. Chấm từng đề tài độc lập theo rubric 100 điểm:\n"
    "   - feasibility (khả thi theo kinh nghiệm tự kể của SV): 0 đến 35 điểm\n"
    "   - career (gắn với định hướng nghề nghiệp của SV): 0 đến 30 điểm\n"
    "   - nature (tính chất đề tài ứng dụng hoặc nghiên cứu): 0 đến 20 điểm\n"
    "   - motivation (động lực thể hiện): 0 đến 15 điểm\n"
    "4. total = feasibility + career + nature + motivation (0 đến 100, bắt buộc bằng tổng các mục).\n"
    "5. reason: lời giải thích ngắn gọn bằng tiếng Việt (1-2 câu).\n"
    "6. CHỈ trả về định dạng JSON thuần túy:\n"
    '{"scores": [{"topic_id": <int>, "feasibility": <num>, "career": <num>, "nature": <num>, '
    '"motivation": <num>, "total": <num>, "reason": "<str>"}]}'
)


class LLMScoreResult(dict):
    """Kết quả chấm điểm LLM cho 1 đề tài, kế thừa dict để tiện truy xuất và tương thích số thực.

    Công thức rubric:
    total = feasibility (0..35) + career (0..30) + nature (0..20) + motivation (0..15).
    """

    @property
    def total(self) -> float:
        return float(self.get("total", 0.0))

    @property
    def reason(self) -> str:
        return str(self.get("reason", ""))

    def __float__(self) -> float:
        return self.total

    def __int__(self) -> int:
        return int(self.total)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return self.total == float(other)
        return super().__eq__(other)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return self.total < float(other)
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return self.total <= float(other)
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return self.total > float(other)
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return self.total >= float(other)
        return NotImplemented


def validate_score_item(item: dict) -> bool:
    """Kiểm tra: tổng các mục = total, 0..100; đúng rubric từng thành phần:
    - feasibility (0..35)
    - career (0..30)
    - nature (0..20)
    - motivation (0..15)
    Công thức: total = feasibility + career + nature + motivation (0 <= total <= 100).
    Nếu tổng sai hoặc vượt thang điểm thì trả về False (bỏ đề tài đó).
    """
    try:
        f = float(item["feasibility"])
        c = float(item["career"])
        n = float(item["nature"])
        m = float(item["motivation"])
        total = float(item["total"])
        if not (0 <= f <= 35 and 0 <= c <= 30 and 0 <= n <= 20 and 0 <= m <= 15):
            return False
        if not (0 <= total <= 100):
            return False
        return abs((f + c + n + m) - total) <= 1e-4
    except (KeyError, TypeError, ValueError):
        return False


def get_cache_key(
    student: Student,
    topic: Topic,
    prompt_version: str = PROMPT_VERSION,
    model: str | None = None,
) -> str:
    """Tính mã băm sha256 cho cache LLMScore theo công thức:
    sha256(profile_version|topic.version|PROMPT_VERSION|model).
    Gắn kèm mã sinh viên và đề tài để bảo đảm khóa duy nhất trong CSDL.
    """
    model = model or getattr(settings, "LLM_MODEL", "openai/gpt-oss-120b")
    pv = getattr(student, "profile_version", 1)
    tv = getattr(topic, "version", 1)
    st_id = getattr(student, "id", None) or getattr(student, "pk", "")
    t_id = getattr(topic, "id", None) or getattr(topic, "pk", "")
    raw = f"{st_id}:{pv}|{t_id}:{tv}|{prompt_version}|{model}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_user_prompt(student: Student, topics: list[Topic]) -> str:
    """Tạo user prompt chứa thông tin sinh viên và danh sách đề tài cần chấm."""
    about_text = student.about.strip() if student.about else "Không có thông tin"
    student_section = f"THÔNG TIN SINH VIÊN:\n- Giới thiệu/định hướng: {about_text}\n"

    topic_items = []
    for t in topics:
        fields = ", ".join(f.name for f in t.fields.all()) if hasattr(t, "fields") else ""
        topic_items.append(
            f"Đề tài #{t.id}:\n- Tên đề tài: {t.title}\n- Lĩnh vực: {fields or 'Chưa rõ'}\n- Mô tả: {t.description}\n"
        )
    topics_section = "DANH SÁCH ĐỀ TÀI:\n" + "\n".join(topic_items)
    return f"{student_section}\n{topics_section}\n\nHãy chấm điểm từng đề tài theo rubric và trả về JSON theo yêu cầu."


def get_endpoint_url(provider: str) -> str:
    """Trả về endpoint URL OpenAI-compatible tương ứng với từng nhà cung cấp."""
    provider = provider.lower()
    if provider == "groq":
        return "https://api.groq.com/openai/v1/chat/completions"
    if provider == "ollama":
        return "http://localhost:11434/v1/chat/completions"
    if provider == "gemini":
        return "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    if provider == "omniroute":  # cổng OmniRoute cục bộ: nhiều nhà cung cấp cùng 1 model, tự chuyển khi hết hạn mức
        return getattr(settings, "LLM_BASE_URL", "") or "http://127.0.0.1:20128/v1/chat/completions"
    return "https://api.groq.com/openai/v1/chat/completions"


def get_request_headers(provider: str, api_key: str) -> dict[str, str]:
    """Tạo headers HTTP chuẩn cho request đến provider."""
    headers = {"Content-Type": "application/json"}
    provider = provider.lower()
    if provider == "groq":
        headers["User-Agent"] = "capstone-advisor/1.0"
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
    elif provider in ("gemini", "ollama", "omniroute") and api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def clean_json_markdown(content: str) -> str:
    """Xóa bỏ markdown code fence ```json ... ``` nếu LLM trả về dạng block code."""
    content = content.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    return content


def parse_llm_response(raw_data: dict) -> list[dict]:
    """Trích xuất và kiểm tra mảng scores từ phản hồi của LLM."""
    if "scores" in raw_data and isinstance(raw_data["scores"], list):
        return raw_data["scores"]
    choices = raw_data.get("choices")
    if not choices or not isinstance(choices, list):
        raise ValueError("Phản hồi LLM thiếu choices hợp lệ")
    content = choices[0].get("message", {}).get("content", "")
    content = clean_json_markdown(content)
    data = json.loads(content)
    if "scores" not in data or not isinstance(data["scores"], list):
        raise ValueError("JSON không chứa danh sách scores")
    return data["scores"]


class FakeLLMProvider:
    """Provider giả lập trả điểm định trước dùng cho kiểm thử, không gọi mạng."""

    call_count: int = 0
    custom_scores: list[dict] | None = None
    custom_response: str | None = None
    should_raise: Exception | None = None
    last_received_topic_ids: list[int] = []

    @classmethod
    def reset(cls) -> None:
        """Khôi phục trạng thái mặc định của FakeLLMProvider."""
        cls.call_count = 0
        cls.custom_scores = None
        cls.custom_response = None
        cls.should_raise = None
        cls.last_received_topic_ids = []

    @classmethod
    def call(cls, student: Student, topics: list[Topic]) -> dict:
        """Sinh phản hồi giả lập cho danh sách đề tài theo rubric 100 điểm."""
        cls.call_count += 1
        cls.last_received_topic_ids = [t.id for t in topics]

        if cls.should_raise:
            raise cls.should_raise

        if cls.custom_response is not None:
            return json.loads(cls.custom_response)

        if cls.custom_scores is not None:
            return {"scores": cls.custom_scores}

        scores = []
        for t in topics:
            f = min(35, 20 + (t.id % 15))
            c = min(30, 15 + (t.id % 15))
            n = min(20, 10 + (t.id % 10))
            m = min(15, 10 + (t.id % 5))
            total = f + c + n + m
            scores.append(
                {
                    "topic_id": t.id,
                    "feasibility": f,
                    "career": c,
                    "nature": n,
                    "motivation": m,
                    "total": total,
                    "reason": f"Đề tài {t.title} phù hợp với định hướng nghề nghiệp và kinh nghiệm.",
                }
            )
        return {"scores": scores}


def call_openai_http(
    student: Student,
    topics: list[Topic],
    provider: str,
    model: str,
    api_key: str,
) -> dict:
    """Gửi yêu cầu HTTP POST chuẩn OpenAI-compatible bằng urllib với temperature=0."""
    if provider in ("groq", "gemini", "omniroute") and not api_key:
        raise ValueError(f"Provider '{provider}' yêu cầu LLM_API_KEY nhưng chưa được cấu hình.")

    url = get_endpoint_url(provider)
    headers = get_request_headers(provider, api_key)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(student, topics)},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    req = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    timeout = getattr(settings, "LLM_TIMEOUT", 30)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def call_provider_with_retry(
    student: Student,
    topics: list[Topic],
    provider: str,
    model: str,
    api_key: str,
) -> list[dict] | None:
    """Gọi LLM provider với cơ chế thử lại tối đa 1 lần nếu gặp lỗi mạng hoặc JSON.
    Sau 1 lần thử lại vẫn lỗi → ghi log và trả về None (để engine tự chia lại trọng số).
    """
    for attempt in range(2):
        try:
            if provider == "fake":
                raw_data = FakeLLMProvider.call(student, topics)
            else:
                raw_data = call_openai_http(student, topics, provider, model, api_key)
            return parse_llm_response(raw_data)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError, KeyError) as e:
            if attempt == 0:
                logger.warning("Gọi LLM lần 1 thất bại (%s: %s). Thử lại lần 2...", type(e).__name__, e)
            else:
                logger.error("Gọi LLM thất bại sau 1 lần thử lại (%s: %s).", type(e).__name__, e)
                return None
        except Exception as e:
            logger.error("Lỗi không xác định khi gọi LLM (%s: %s).", type(e).__name__, e)
            return None
    return None


def process_llm_items(
    student: Student,
    topics_by_id: dict[int, Topic],
    keys_by_id: dict[int, str],
    items: list[dict],
    model: str,
) -> tuple[dict[int, LLMScoreResult], set[int]]:
    """Xử lý và lưu cache các mục điểm LLM trả về:
    - Điểm hợp lệ: lưu vào LLMScore cache và đưa vào kết quả.
    - Điểm sai tổng (rubric không khớp hoặc ngoài 0..100): đưa vào invalid_topic_ids để loại bỏ.
    """
    valid_scores = {}
    invalid_topic_ids = set()
    for item in items:
        try:
            t_id = int(item["topic_id"])
        except (KeyError, TypeError, ValueError):
            continue
        if t_id not in topics_by_id:
            continue
        if validate_score_item(item):
            topic = topics_by_id[t_id]
            cache_k = keys_by_id[t_id]
            LLMScore.objects.update_or_create(
                cache_key=cache_k,
                defaults={
                    "student": student,
                    "topic": topic,
                    "score_json": item,
                    "model": model,
                    "prompt_version": PROMPT_VERSION,
                },
            )
            valid_scores[t_id] = LLMScoreResult(item)
        else:
            invalid_topic_ids.add(t_id)
    return valid_scores, invalid_topic_ids


def batch_score_llm(
    student: Student,
    topics: list[Topic],
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> tuple[dict[int, LLMScoreResult], set[int]]:
    """Chấm điểm LLM hàng loạt cho danh sách đề tài của sinh viên (Top-K):
    1. Kiểm tra cache LLMScore theo sha256(profile_version|topic.version|PROMPT_VERSION|model).
    2. Nếu còn đề tài chưa cache: xáo trộn ngẫu nhiên thứ tự đề tài trước khi gửi.
    3. Gọi API với temperature=0.
    4. Kiểm tra tổng các mục = total, 0..100: sai thì bỏ đề tài đó (invalid_topic_ids).
    5. Trả về (scored_dict, invalid_topic_ids).
    """
    if not topics:
        return {}, set()

    provider = (provider or getattr(settings, "LLM_PROVIDER", "groq")).lower()
    model = model or getattr(settings, "LLM_MODEL", "openai/gpt-oss-120b")
    api_key = getattr(settings, "LLM_API_KEY", "") if api_key is None else api_key

    topics_by_id = {t.id: t for t in topics}
    keys_by_id = {t.id: get_cache_key(student, t, PROMPT_VERSION, model) for t in topics}

    scored_dict: dict[int, LLMScoreResult] = {}
    cached_entries = LLMScore.objects.filter(cache_key__in=keys_by_id.values())
    cached_map = {ce.cache_key: ce for ce in cached_entries}

    uncached_topics = []
    for t in topics:
        k = keys_by_id[t.id]
        if k in cached_map:
            scored_dict[t.id] = LLMScoreResult(cached_map[k].score_json)
        else:
            uncached_topics.append(t)

    if not uncached_topics:
        return scored_dict, set()

    # Xáo trộn ngẫu nhiên thứ tự đề tài trước khi gửi (chống thiên lệch vị trí)
    shuffled_topics = list(uncached_topics)
    random.shuffle(shuffled_topics)

    items = call_provider_with_retry(student, shuffled_topics, provider, model, api_key)
    if items is None:
        return scored_dict, set()

    valid_scores, invalid_ids = process_llm_items(student, topics_by_id, keys_by_id, items, model)
    scored_dict.update(valid_scores)
    return scored_dict, invalid_ids


def score_pair(
    student: Student,
    topic: Topic,
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> LLMScoreResult | None:
    """Tính bù M5 cho 1 cặp (sinh viên, đề tài) theo rubric 100 điểm.
    Dùng khi sinh viên chọn nguyện vọng ngoài Top-K ứng viên.
    Trả về LLMScoreResult (chứa total, reason...) hoặc None nếu lỗi mạng/JSON hoặc tổng sai.
    """
    if not getattr(settings, "RECOMMEND_LLM", True):
        return None

    provider = (provider or getattr(settings, "LLM_PROVIDER", "groq")).lower()
    model = model or getattr(settings, "LLM_MODEL", "openai/gpt-oss-120b")
    api_key = getattr(settings, "LLM_API_KEY", "") if api_key is None else api_key

    cache_k = get_cache_key(student, topic, PROMPT_VERSION, model)
    cached = LLMScore.objects.filter(cache_key=cache_k).first()
    if cached:
        return LLMScoreResult(cached.score_json)

    items = call_provider_with_retry(student, [topic], provider, model, api_key)
    if not items:
        return None

    item = next((it for it in items if int(it.get("topic_id", -1)) == topic.id), None)
    if not item or not validate_score_item(item):
        logger.warning("Điểm LLM cho đề tài #%s không hợp lệ hoặc tổng sai rubric.", topic.id)
        return None

    LLMScore.objects.update_or_create(
        cache_key=cache_k,
        defaults={
            "student": student,
            "topic": topic,
            "score_json": item,
            "model": model,
            "prompt_version": PROMPT_VERSION,
        },
    )
    return LLMScoreResult(item)
