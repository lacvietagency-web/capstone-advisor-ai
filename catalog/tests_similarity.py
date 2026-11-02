"""Phát hiện đề tài trùng + tư vấn khoá trước (ý kiến GVHD 22/10/2026).

Dùng mô hình ngữ nghĩa GIẢ (bag-of-words chuẩn hoá) để chạy nhanh, không tải SentenceTransformer 470 MB:
hai câu cùng từ → cosine 1, không chung từ → 0. Nhờ đó kiểm được logic ngưỡng và xếp hạng.
"""

import io
import re

import numpy as np
from django.test import TestCase, override_settings

from catalog import similarity
from catalog.models import ArchivedTopic, Lecturer, Topic
from catalog.similarity import duplicate_pairs, improvement_advice, similar_archived, similar_open_topics
from recommend.engine import SemanticModel


def _fake_vec(text):
    vocab = sorted(set(re.findall(r"\w+", text.lower())))
    full = "python web học máy chatbot dữ liệu di động bán sách phim thư viện gợi ý nhận diện"
    axes = full.split()
    v = np.array([1.0 if w in vocab else 0.0 for w in axes])
    n = np.linalg.norm(v)
    return v / n if n else v


@override_settings(RECOMMEND_SEMANTIC=True, RECOMMEND_LLM=False)
class SimilarityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = __import__("accounts.models", fromlist=["User"]).User
        cls.lec = Lecturer.objects.create(user=u.objects.create_user("gvx", role=u.Role.LECTURER))
        cls.lec2 = Lecturer.objects.create(user=u.objects.create_user("gvy", role=u.Role.LECTURER))
        cls.t1 = Topic.objects.create(
            lecturer=cls.lec, title="Hệ thống gợi ý phim", description="gợi ý phim bằng học máy"
        )
        cls.t2 = Topic.objects.create(
            lecturer=cls.lec2, title="Gợi ý phim học máy", description="gợi ý phim bằng học máy"
        )
        cls.t3 = Topic.objects.create(lecturer=cls.lec, title="Chatbot web", description="chatbot web python")
        cls.arch = ArchivedTopic.objects.create(
            title="Hệ thống gợi ý phim", description="gợi ý phim bằng học máy", year=2023
        )

    def setUp(self):
        SemanticModel._topic_vecs.clear()
        SemanticModel._text_vecs.clear()
        self._orig = SemanticModel.encode
        SemanticModel.encode = classmethod(lambda cls, texts: np.array([_fake_vec(t) for t in texts]))

    def tearDown(self):
        SemanticModel.encode = self._orig

    def test_similar_open_topics_flags_near_duplicate(self):
        res = similar_open_topics(self.t1, Topic.objects.all())
        titles = [t.title for t, _ in res]
        self.assertIn("Gợi ý phim học máy", titles)  # t2 trùng nội dung
        self.assertNotIn("Chatbot web", titles)  # t3 khác hẳn
        self.assertGreaterEqual(res[0][1], similarity.DUP_THRESHOLD)

    def test_similar_open_excludes_self(self):
        res = similar_open_topics(self.t1, Topic.objects.all())
        self.assertNotIn(self.t1.pk, [t.pk for t, _ in res])

    def test_duplicate_pairs(self):
        pairs = duplicate_pairs(Topic.objects.all())
        self.assertTrue(any({a.pk, b.pk} == {self.t1.pk, self.t2.pk} for a, b, _ in pairs))

    def test_archived_advice_heuristic_when_llm_off(self):
        adv = improvement_advice(self.t1, similar_archived(self.t1, ArchivedTopic.objects.all()))
        self.assertIsNotNone(adv)
        self.assertEqual(adv["match"].pk, self.arch.pk)
        self.assertIsNone(adv["llm"])  # LLM tắt
        self.assertTrue(adv["points"])  # có gợi ý heuristic

    def test_no_false_positive(self):
        self.assertEqual(similar_archived(self.t3, ArchivedTopic.objects.all()), [])


@override_settings(RECOMMEND_SEMANTIC=False)
class DuplicatesViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command

        call_command("seed_demo", students=5, lecturers=3, topics=8, verbosity=0)

    def test_permission(self):
        self.assertEqual(self.client.get("/khoa/ra-soat-trung-lap/").status_code, 302)  # khách → đăng nhập
        self.client.login(username="sv001", password="123456")
        self.assertEqual(self.client.get("/khoa/ra-soat-trung-lap/").status_code, 403)
        self.client.logout()
        self.client.login(username="khoa01", password="123456")
        r = self.client.get("/khoa/ra-soat-trung-lap/")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.context["enabled"])  # SEMANTIC tắt → không tải mô hình

    def test_them_de_tai_khoa_truoc_idempotent(self):
        from django.core.management import call_command

        ArchivedTopic.objects.all().delete()
        t = Topic.objects.first()
        call_command("them_de_tai_khoa_truoc", tu_de_tai=t.pk, stdout=io.StringIO())
        n = ArchivedTopic.objects.count()
        self.assertEqual(n, 5)
        call_command("them_de_tai_khoa_truoc", tu_de_tai=t.pk, stdout=io.StringIO())  # chạy lại: không trùng
        self.assertEqual(ArchivedTopic.objects.count(), n)
        self.assertTrue(ArchivedTopic.objects.filter(title=t.title, year=2024).exists())
