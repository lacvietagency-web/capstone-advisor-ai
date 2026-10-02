"""KIỂM THỬ NGHIỆM THU cho Issue #3 (Claude viết trước, Gemini phải làm cho đạt).

Giao diện bắt buộc của module allocate/solver.py (dữ liệu thuần Python, dễ kiểm thử):
    prefs:  {sv: [đề_tài_NV1, NV2, NV3]}        scores: {(sv, đề_tài): 0..100}
    cap:    {đề_tài: sức chứa}                  owner:  {đề_tài: giảng_viên}
    quota:  {giảng_viên: chỉ tiêu}              gpa:    {sv: GPA}
    solve_ilp(prefs, scores, cap, owner, quota, gpa, alpha=0.4, beta=0.6, lam=2.0, eps=1e-3) -> {sv: đề_tài hoặc None}
    solve_greedy(prefs, scores, cap, owner, quota, gpa) -> {sv: đề_tài hoặc None}
    metrics(assign, prefs, scores, cap, owner, quota) -> dict: assigned_rate, nv1_rate, top3_rate, mean_rank,
                                                               avg_match, p10_match, quota_violations
Lệnh: python manage.py allocate_period --algorithm ILP|GREEDY  → lưu Allocation (DRAFT) cho đợt đang mở/đã đóng mới nhất.
"""
from unittest import skipUnless

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings

from allocate import solver

READY = all(hasattr(solver, f) for f in ("solve_ilp", "solve_greedy", "metrics"))   # chưa có lời giải → bỏ qua, không làm đỏ CI
if READY:
    from allocate.solver import metrics, solve_greedy, solve_ilp


def base(**kw):
    d = dict(prefs={}, scores={}, cap={}, owner={}, quota={}, gpa={})
    d.update(kw)
    return d


@skipUnless(READY, "chờ Issue #3: allocate/solver.py")
class SolverTests(SimpleTestCase):
    def test_contention_both_assigned(self):
        """2 SV cùng muốn A (1 chỗ); SV điểm cao hơn được A, SV kia được NV2."""
        d = base(prefs={"s1": ["A", "B"], "s2": ["A", "B"]}, scores={("s1", "A"): 90, ("s2", "A"): 60, ("s1", "B"): 70, ("s2", "B"): 70},
                 cap={"A": 1, "B": 1}, owner={"A": "g1", "B": "g2"}, quota={"g1": 5, "g2": 5}, gpa={"s1": 3, "s2": 3})
        a = solve_ilp(**d)
        self.assertEqual(a, {"s1": "A", "s2": "B"})

    def test_ilp_beats_greedy_on_coverage(self):
        """Ca kinh điển: Greedy xếp s1 (điểm cao) vào A → s2 (chỉ chọn A) trắng tay. ILP đẩy s1 sang B để xếp đủ cả hai."""
        d = base(prefs={"s1": ["A", "B"], "s2": ["A"]}, scores={("s1", "A"): 95, ("s1", "B"): 80, ("s2", "A"): 70},
                 cap={"A": 1, "B": 1}, owner={"A": "g1", "B": "g1"}, quota={"g1": 5}, gpa={"s1": 3.5, "s2": 3.0})
        self.assertIsNone(solve_greedy(**d)["s2"])
        self.assertEqual(solve_ilp(**d), {"s1": "B", "s2": "A"})

    def test_lecturer_quota_respected(self):
        d = base(prefs={f"s{i}": ["A", "B"] for i in range(4)}, scores={(f"s{i}", t): 50 for i in range(4) for t in "AB"},
                 cap={"A": 3, "B": 3}, owner={"A": "g1", "B": "g1"}, quota={"g1": 2}, gpa={f"s{i}": 3 for i in range(4)})
        a = solve_ilp(**d)
        self.assertEqual(sum(1 for t in a.values() if t), 2)
        self.assertEqual(metrics(a, d["prefs"], d["scores"], d["cap"], d["owner"], d["quota"])["quota_violations"], 0)

    def test_never_outside_preferences(self):
        d = base(prefs={"s1": ["A"], "s2": ["A"]}, scores={("s1", "A"): 80, ("s2", "A"): 70, ("s1", "C"): 99, ("s2", "C"): 99},
                 cap={"A": 1, "C": 5}, owner={"A": "g1", "C": "g1"}, quota={"g1": 10}, gpa={"s1": 3, "s2": 3})
        a = solve_ilp(**d)
        for s, t in a.items():
            self.assertTrue(t is None or t in d["prefs"][s])
        self.assertEqual(sorted(a.values(), key=str), ["A", None])

    def test_tie_break_by_gpa(self):
        d = base(prefs={"s1": ["A"], "s2": ["A"]}, scores={("s1", "A"): 70, ("s2", "A"): 70},
                 cap={"A": 1}, owner={"A": "g1"}, quota={"g1": 5}, gpa={"s1": 2.5, "s2": 3.6})
        self.assertEqual(solve_ilp(**d), {"s1": None, "s2": "A"})

    def test_metrics(self):
        prefs = {"s1": ["A", "B"], "s2": ["A", "B"], "s3": ["C"]}
        scores = {("s1", "A"): 80, ("s2", "B"): 60}
        m = metrics({"s1": "A", "s2": "B", "s3": None}, prefs, scores, {"A": 1, "B": 1, "C": 1}, {"A": "g", "B": "g", "C": "g"}, {"g": 5})
        self.assertAlmostEqual(m["assigned_rate"], 2 / 3)
        self.assertAlmostEqual(m["nv1_rate"], 1 / 3)
        self.assertAlmostEqual(m["top3_rate"], 2 / 3)
        self.assertAlmostEqual(m["mean_rank"], 1.5)
        self.assertAlmostEqual(m["avg_match"], 70)
        self.assertEqual(m["quota_violations"], 0)


@override_settings(RECOMMEND_SEMANTIC=False)
@skipUnless(READY, "chờ Issue #3")
class CommandTests(TestCase):
    def test_allocate_period_saves_drafts(self):
        from allocate.models import Allocation
        call_command("seed_demo", students=20, lecturers=4, topics=10, verbosity=0)
        call_command("recommend_all", verbosity=0)
        call_command("allocate_period", algorithm="ILP", verbosity=0)
        self.assertEqual(Allocation.objects.count(), 20)
        self.assertTrue(all(a.status == "DRAFT" and a.source == "ILP" for a in Allocation.objects.all()))
