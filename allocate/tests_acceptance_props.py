"""Nghiệm thu P0 #2–#4 — kiểm thử dựa trên thuộc tính (Hypothesis) cho bộ phân công, so với nghiệm tối ưu vét cạn.

Hypothesis sinh ngẫu nhiên hàng trăm bài toán nhỏ (SV, đề tài, GV, sức chứa, chỉ tiêu, NV, điểm, GPA) và tự rút gọn về
phản ví dụ nhỏ nhất nếu một bất biến sai. Số lần sinh mỗi bất biến ghi ở @settings(max_examples=...).
"""

import itertools

from django.test import SimpleTestCase
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from allocate.solver import compute_utility, solve_greedy, solve_ilp

ALPHA, BETA, EPS = 0.4, 0.6, 1e-3


@st.composite
def instances(draw, max_students=8):
    n_lec = draw(st.integers(1, 3))
    n_top = draw(st.integers(1, 5))
    n_stu = draw(st.integers(0, max_students))
    topics = [f"t{i}" for i in range(n_top)]
    owner = {t: f"g{draw(st.integers(0, n_lec - 1))}" for t in topics}
    cap = {t: draw(st.integers(0, 3)) for t in topics}
    quota = {f"g{g}": draw(st.integers(0, 4)) for g in range(n_lec)}
    prefs, scores, gpa = {}, {}, {}
    for i in range(n_stu):
        s = f"s{i}"
        prefs[s] = draw(st.lists(st.sampled_from(topics), max_size=3, unique=True))
        gpa[s] = draw(st.floats(0, 4, allow_nan=False))
        for t in prefs[s]:
            scores[(s, t)] = draw(st.floats(0, 100, allow_nan=False))
    return prefs, scores, cap, owner, quota, gpa


def _check_feasible(tc, assign, prefs, cap, owner, quota):
    tc.assertEqual(set(assign), set(prefs))  # mọi SV đều có mặt trong kết quả (đề tài hoặc None)
    per_topic, per_lec = {}, {}
    for s, t in assign.items():
        if t is None:
            continue
        tc.assertIn(t, prefs[s], "xếp SV vào đề tài không nằm trong NV")
        per_topic[t] = per_topic.get(t, 0) + 1
        per_lec[owner[t]] = per_lec.get(owner[t], 0) + 1
    for t, k in per_topic.items():
        tc.assertLessEqual(k, cap[t], f"vượt sức chứa {t}")
    for g, k in per_lec.items():
        tc.assertLessEqual(k, quota.get(g, 0), f"vượt chỉ tiêu {g}")


def _objective(assign, prefs, scores, gpa):
    return sum(compute_utility(s, t, prefs[s].index(t) + 1, scores, gpa, ALPHA, BETA, EPS) for s, t in assign.items() if t)


def _brute_force(prefs, scores, cap, owner, quota, gpa):
    """Duyệt hết mọi cách xếp hợp lệ: trả về (số SV xếp tối đa, mục tiêu tốt nhất trong các cách đạt số đó)."""
    students = list(prefs)
    best = (0, 0.0)
    for combo in itertools.product(*[[None, *prefs[s]] for s in students]):
        per_topic, per_lec, ok = {}, {}, True
        for t in combo:
            if t is None:
                continue
            per_topic[t] = per_topic.get(t, 0) + 1
            per_lec[owner[t]] = per_lec.get(owner[t], 0) + 1
            if per_topic[t] > cap[t] or per_lec[owner[t]] > quota.get(owner[t], 0):
                ok = False
                break
        if not ok:
            continue
        assign = dict(zip(students, combo, strict=True))
        cand = (sum(t is not None for t in combo), _objective(assign, prefs, scores, gpa))
        if cand[0] > best[0] or (cand[0] == best[0] and cand[1] > best[1] + 1e-9):
            best = cand
    return best


class AllocationProperties(SimpleTestCase):
    @settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    @given(instances())
    def test_ilp_and_greedy_always_feasible(self, inst):
        """Bất biến: mỗi SV ≤ 1 đề tài, chỉ trong NV của mình, không vượt sức chứa đề tài và chỉ tiêu GV."""
        prefs, scores, cap, owner, quota, gpa = inst
        _check_feasible(self, solve_ilp(prefs, scores, cap, owner, quota, gpa), prefs, cap, owner, quota)
        _check_feasible(self, solve_greedy(prefs, scores, cap, owner, quota, gpa), prefs, cap, owner, quota)

    @settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    @given(instances())
    def test_ilp_assigns_at_least_as_many_as_greedy(self, inst):
        prefs, scores, cap, owner, quota, gpa = inst
        n_ilp = sum(t is not None for t in solve_ilp(prefs, scores, cap, owner, quota, gpa).values())
        n_greedy = sum(t is not None for t in solve_greedy(prefs, scores, cap, owner, quota, gpa).values())
        self.assertGreaterEqual(n_ilp, n_greedy)

    @settings(max_examples=150, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    @given(instances(max_students=6))
    def test_ilp_matches_brute_force_optimum(self, inst):
        """ILP = tối ưu toàn cục: xếp được nhiều SV nhất có thể, và trong các cách đó có độ thoả dụng lớn nhất."""
        prefs, scores, cap, owner, quota, gpa = inst
        assign = solve_ilp(prefs, scores, cap, owner, quota, gpa)
        best_n, best_obj = _brute_force(prefs, scores, cap, owner, quota, gpa)
        self.assertEqual(sum(t is not None for t in assign.values()), best_n)
        self.assertAlmostEqual(_objective(assign, prefs, scores, gpa), best_obj, places=6)

    def test_boundary_datasets(self):
        """#4 dữ liệu biên: 0 SV; 1 GV; đề tài sức chứa 0; cả lớp chọn cùng 1 đề tài."""
        self.assertEqual(solve_ilp({}, {}, {"t0": 1}, {"t0": "g0"}, {"g0": 1}, {}), {})
        prefs = {f"s{i}": ["t0"] for i in range(10)}
        scores = {(s, "t0"): 80.0 for s in prefs}
        gpa = {s: 3.0 for s in prefs}
        one = solve_ilp(prefs, scores, {"t0": 2}, {"t0": "g0"}, {"g0": 5}, gpa)
        self.assertEqual(sum(t is not None for t in one.values()), 2)  # cả lớp 1 đề tài sức chứa 2 → đúng 2 SV
        zero = solve_ilp(prefs, scores, {"t0": 0}, {"t0": "g0"}, {"g0": 5}, gpa)
        self.assertTrue(all(t is None for t in zero.values()))
        capped = solve_ilp(prefs, scores, {"t0": 9}, {"t0": "g0"}, {"g0": 3}, gpa)
        self.assertEqual(sum(t is not None for t in capped.values()), 3)  # chỉ tiêu GV chặn trước sức chứa
