"""M5 do Claude chấm (LLM_PROVIDER=claude): xuất đề bài → Claude chấm đúng rubric 100 điểm → nạp cache LLMScore.

  python manage.py cham_m5_claude xuat de-bai.json   # mỗi SV: prompt y hệt bản gọi API, chỉ gồm đề tài chưa có M5
  python manage.py cham_m5_claude nap diem.json      # {"scores": [{student_id, topic_id, feasibility, career,
                                                     #   nature, motivation, total, reason}]} → cache + tính lại
Điểm sai rubric (tổng lệch, vượt thang) bị bỏ, giống khi API trả sai.
"""

import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.models import Preference, Student, Topic
from recommend.engine import compute_stage1_candidates
from recommend.llm import PROMPT_VERSION, SYSTEM_PROMPT, build_user_prompt, get_cache_key, validate_score_item
from recommend.models import LLMScore
from recommend.services import open_topics, refresh_student


class Command(BaseCommand):
    help = "Xuất đề bài / nạp điểm M5 do Claude chấm vào cache LLMScore."

    def add_arguments(self, parser):
        parser.add_argument("viec", choices=["xuat", "nap"])
        parser.add_argument("tep")

    def handle(self, viec, tep, **opts):
        if viec == "xuat":
            self._xuat(tep, settings.LLM_MODEL)
        else:
            self._nap(tep, settings.LLM_MODEL)

    def _xuat(self, tep, model):
        topics = open_topics()
        out = {"system": SYSTEM_PROMPT, "model": model, "students": []}
        n = 0
        for st in Student.objects.select_related("user"):
            eligible = [c.topic for c in compute_stage1_candidates(st, topics, top_k=None, semantic=False)]
            chosen = Preference.objects.filter(student=st).values_list("topic_id", flat=True)
            todo = eligible + [t for t in Topic.objects.filter(pk__in=chosen) if t not in eligible]
            cached = set(LLMScore.objects.filter(student=st).values_list("cache_key", flat=True))
            todo = [t for t in todo if get_cache_key(st, t, PROMPT_VERSION, model) not in cached]
            if todo:
                out["students"].append(
                    {"student_id": st.pk, "username": st.user.username, "prompt": build_user_prompt(st, todo)}
                )
                n += len(todo)
        with open(tep, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        self.stdout.write(f"Đã xuất {n} cặp SV–đề tài chưa có M5 ({len(out['students'])} SV) → {tep}")

    def _nap(self, tep, model):
        with open(tep, encoding="utf-8") as f:
            items = json.load(f)["scores"]
        ok, bad, touched = 0, [], set()
        for it in items:
            st = Student.objects.filter(pk=it.get("student_id")).first()
            topic = Topic.objects.filter(pk=it.get("topic_id")).first()
            if not st or not topic or not validate_score_item(it):
                bad.append((it.get("student_id"), it.get("topic_id")))
                continue
            LLMScore.objects.update_or_create(
                cache_key=get_cache_key(st, topic, PROMPT_VERSION, model),
                defaults={
                    "student": st,
                    "topic": topic,
                    "score_json": it,
                    "model": model,
                    "prompt_version": PROMPT_VERSION,
                },
            )
            ok += 1
            touched.add(st.pk)
        for st in Student.objects.filter(pk__in=touched):
            refresh_student(st, llm=True)  # đọc cache vừa nạp → M5 vào điểm cuối và thứ hạng gợi ý
        if bad:
            self.stderr.write(f"Bỏ {len(bad)} điểm sai rubric/không tìm thấy: {bad[:10]}")
        if items and not ok:
            raise CommandError("Không nạp được điểm nào.")
        self.stdout.write(f"Đã nạp {ok} điểm M5, tính lại gợi ý cho {len(touched)} SV.")
