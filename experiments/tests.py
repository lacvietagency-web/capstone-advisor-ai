"""Kiểm thử tự động cho gói mô-đun thực nghiệm experiments.

Kiểm thử:
1. Các hàm đo lường IR: Hit@K, MRR, NDCG@K.
2. Các hàm đo lường độ ổn định LLM: MAE, Spearman Rank Correlation.
3. Kịch bản phân công thực nghiệm mô phỏng RQ3 (Greedy vs ILP).
"""

from django.test import TestCase

from experiments.metrics import (
    compute_hit_at_k,
    compute_mae,
    compute_mrr,
    compute_ndcg_at_k,
    compute_spearman,
)
from experiments.rq3_allocation import generate_benchmark_instance, run_benchmark_trial


class ExperimentMetricsTests(TestCase):
    """Kiểm thử tính đúng đắn của các công thức đo lường trong experiments.metrics."""

    def test_hit_at_k(self):
        """Hit@K trả về 1.0 nếu có ít nhất 1 mục phù hợp trong Top K, ngược lại 0.0."""
        ranked = [10, 20, 30, 40, 50, 60]
        self.assertEqual(compute_hit_at_k(ranked, {30}, k=5), 1.0)
        self.assertEqual(compute_hit_at_k(ranked, {60}, k=5), 0.0)
        self.assertEqual(compute_hit_at_k(ranked, set(), k=5), 0.0)

    def test_mrr(self):
        """MRR trả về nghịch đảo vị trí của mục phù hợp đầu tiên."""
        ranked = [10, 20, 30, 40]
        self.assertAlmostEqual(compute_mrr(ranked, {20}), 0.5)
        self.assertAlmostEqual(compute_mrr(ranked, {10}), 1.0)
        self.assertEqual(compute_mrr(ranked, {99}), 0.0)
        self.assertEqual(compute_mrr(ranked, set()), 0.0)

    def test_ndcg_at_k(self):
        """NDCG@K trả về điểm chuẩn hóa tích lũy chiết khấu theo log2."""
        ranked = [10, 20, 30]
        # Nếu mục đầu tiên đúng và tập rel chỉ có {10} -> NDCG = 1.0
        self.assertAlmostEqual(compute_ndcg_at_k(ranked, {10}, k=3), 1.0)
        # Nếu không có mục nào đúng -> NDCG = 0.0
        self.assertAlmostEqual(compute_ndcg_at_k(ranked, {99}, k=3), 0.0)
        self.assertEqual(compute_ndcg_at_k(ranked, set(), k=3), 0.0)

    def test_mae_and_spearman(self):
        """MAE đo sai số tuyệt đối và Spearman đo độ tương quan thứ hạng."""
        y1 = [10.0, 20.0, 30.0]
        y2 = [12.0, 18.0, 30.0]
        # |10-12| + |20-18| + |30-30| = 2 + 2 + 0 = 4 / 3 = 1.3333
        self.assertAlmostEqual(compute_mae(y1, y2), 4.0 / 3.0)
        # Thứ hạng giữ nguyên 1, 2, 3 -> Spearman = 1.0
        self.assertAlmostEqual(compute_spearman(y1, y2), 1.0)

        # Thứ hạng đảo ngược -> Spearman = -1.0
        y_rev = [30.0, 20.0, 10.0]
        self.assertAlmostEqual(compute_spearman(y1, y_rev), -1.0)

        # Mảng rỗng hoặc sai kích thước
        self.assertEqual(compute_mae([], []), 0.0)
        self.assertEqual(compute_spearman([], []), 1.0)


class AllocationBenchmarkTests(TestCase):
    """Kiểm thử quy trình sinh dữ liệu và giải phân công RQ3."""

    def test_generate_and_solve_instance(self):
        """Bộ sinh dữ liệu phân công tạo đủ trường và ILP/Greedy giải không vi phạm."""
        prefs, scores, cap, owner, quota, gpa = generate_benchmark_instance(num_students=20, seed=42)
        self.assertEqual(len(prefs), 20)
        self.assertEqual(len(gpa), 20)

        # Chạy thử Greedy
        m_greedy = run_benchmark_trial(prefs, scores, cap, owner, quota, gpa, algorithm="GREEDY")
        self.assertEqual(m_greedy["quota_violations"], 0)
        self.assertGreater(m_greedy["assigned_rate"], 0.0)

        # Chạy thử ILP
        m_ilp = run_benchmark_trial(prefs, scores, cap, owner, quota, gpa, algorithm="ILP", alpha=0.4, beta=0.6)
        self.assertEqual(m_ilp["quota_violations"], 0)
        self.assertGreaterEqual(m_ilp["assigned_rate"], m_greedy["assigned_rate"])


class BaselineAlgorithmTests(TestCase):
    """RQ3b: Gale-Shapley phải ổn định (0 cặp chặn) và hợp lệ; GA hợp lệ và không vượt nghiệm tối ưu ILP."""

    def test_gale_shapley_stable_and_feasible(self):
        from allocate.solver import metrics
        from experiments.baselines import blocking_pairs, solve_gale_shapley

        for seed in (1, 2, 3):
            inst = generate_benchmark_instance(60, seed=seed)
            a = solve_gale_shapley(*inst)
            self.assertEqual(metrics(a, *inst[:5])["quota_violations"], 0)
            self.assertEqual(blocking_pairs(a, *inst), 0)

    def test_blocking_pairs_detects_instability(self):
        from experiments.baselines import blocking_pairs

        # 1 đề tài 1 chỗ; GV thích s2 (điểm cao hơn) nhưng đề tài lại giao s1 → (s2, t) là cặp chặn
        prefs, scores = {1: ["t"], 2: ["t"]}, {(1, "t"): 50.0, (2, "t"): 90.0}
        inst = (prefs, scores, {"t": 1}, {"t": "g"}, {"g": 1}, {1: 3.0, 2: 3.0})
        self.assertEqual(blocking_pairs({1: "t", 2: None}, *inst), 1)
        self.assertEqual(blocking_pairs({1: None, 2: "t"}, *inst), 0)

    def test_genetic_feasible_and_not_above_ilp(self):
        from allocate.solver import metrics, solve_ilp
        from experiments.baselines import solve_genetic
        from experiments.rq3b_four_algorithms import objective

        inst = generate_benchmark_instance(40, seed=5)
        ga = solve_genetic(*inst, generations=40, seed=1)
        self.assertEqual(metrics(ga, *inst[:5])["quota_violations"], 0)
        ilp = solve_ilp(*inst)
        prefs, scores, gpa = inst[0], inst[1], inst[5]
        self.assertLessEqual(objective(ga, prefs, scores, gpa), objective(ilp, prefs, scores, gpa) + 1e-6)
