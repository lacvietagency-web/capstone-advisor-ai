"""Nghiệm thu P0 #2 — kiểm thử thuộc tính (Hypothesis) cho công thức M1–M3, điểm tổng và AHP.

Công thức M1–M3 chỉ đọc vài thuộc tính của hồ sơ/đề tài nên dùng đối tượng giả gọn, không cần CSDL.
"""

from types import SimpleNamespace

import numpy as np
from django.test import SimpleTestCase
from hypothesis import given, settings
from hypothesis import strategies as st

from recommend.ahp import calculate_ahp
from recommend.engine import Candidate, m1_skill, m2_academic, m3_field


def _all(items):
    return SimpleNamespace(all=lambda: list(items))


@st.composite
def skill_case(draw):
    n = draw(st.integers(0, 5))
    req = [
        SimpleNamespace(
            skill_id=i,
            weight=draw(st.floats(0.1, 5)),
            required_level=draw(st.integers(1, 5)),
            skill=SimpleNamespace(name=f"k{i}"),
        )
        for i in range(n)
    ]
    have = {i: draw(st.integers(0, 5)) for i in range(n) if draw(st.booleans())}
    return req, have


class ScoreProperties(SimpleTestCase):
    @settings(max_examples=300, deadline=None)
    @given(skill_case())
    def test_m1_in_range_and_full_when_all_met(self, case):
        req, have = case
        score, missing = m1_skill(SimpleNamespace(skills=have), SimpleNamespace(skills=_all(req)))
        self.assertTrue(0 <= score <= 100 + 1e-9)
        all_met = all(have.get(r.skill_id, 0) >= r.required_level for r in req)
        self.assertEqual(all_met, not missing)
        if all_met:
            self.assertAlmostEqual(score, 100.0)

    @settings(max_examples=300, deadline=None)
    @given(skill_case(), st.integers(0, 4))
    def test_m1_never_drops_when_student_improves(self, case, boost_id):
        req, have = case
        topic = SimpleNamespace(skills=_all(req))
        before, _ = m1_skill(SimpleNamespace(skills=have), topic)
        better = {**have, boost_id: min(5, have.get(boost_id, 0) + 1)}
        after, _ = m1_skill(SimpleNamespace(skills=better), topic)
        self.assertGreaterEqual(after + 1e-9, before)

    @settings(max_examples=300, deadline=None)
    @given(
        st.floats(0, 4),
        st.dictionaries(st.integers(0, 6), st.floats(0, 10), max_size=6),
        st.lists(st.integers(0, 3), max_size=4),
    )
    def test_m2_in_range(self, gpa, courses, field_ids):
        p = SimpleNamespace(gpa=gpa, courses=courses, course_fields={c: c % 4 for c in courses})
        topic = SimpleNamespace(fields=_all([SimpleNamespace(id=f) for f in field_ids]), prerequisites=_all([]))
        self.assertTrue(0 <= m2_academic(p, topic) <= 100 + 1e-9)

    @settings(max_examples=300, deadline=None)
    @given(st.dictionaries(st.integers(0, 6), st.integers(0, 3)), st.lists(st.integers(0, 6), max_size=4, unique=True))
    def test_m3_in_range(self, interests, field_ids):
        score = m3_field(
            SimpleNamespace(interests=interests),
            SimpleNamespace(fields=_all([SimpleNamespace(id=f) for f in field_ids])),
        )
        self.assertTrue(0 <= score <= 100 + 1e-9)

    @settings(max_examples=300, deadline=None)
    @given(
        st.dictionaries(
            st.sampled_from(["skill", "academic", "field", "semantic", "llm"]),
            st.one_of(st.none(), st.floats(0, 100)),
            min_size=1,
        )
    )
    def test_final_score_between_component_scores(self, scores):
        weights = {"skill": 0.35, "academic": 0.2, "field": 0.15, "semantic": 0.2, "llm": 0.1}
        have = [v for v in scores.values() if v is not None]
        final = Candidate(topic=None, scores=scores).final(weights)
        if have:
            self.assertTrue(min(have) - 1e-9 <= final <= max(have) + 1e-9)
        else:
            self.assertEqual(final, 0.0)


class AHPProperties(SimpleTestCase):
    @settings(max_examples=200, deadline=None)
    @given(st.lists(st.floats(0.05, 20), min_size=5, max_size=5))
    def test_consistent_matrix_recovers_weights(self, w):
        """Ma trận nhất quán a_ij = w_i / w_j → CR ≈ 0 và trọng số khôi phục đúng w đã chuẩn hoá."""
        w = np.array(w)
        res = calculate_ahp(w[:, None] / w[None, :])
        got = np.array(list(res.weights.values()))
        self.assertAlmostEqual(got.sum(), 1.0, places=9)
        np.testing.assert_allclose(got, w / w.sum(), atol=1e-6)
        self.assertLess(res.cr, 1e-6)
        self.assertTrue(res.is_consistent)

    @settings(max_examples=200, deadline=None)
    @given(st.lists(st.sampled_from([1 / 9, 1 / 7, 1 / 5, 1 / 3, 1, 3, 5, 7, 9]), min_size=10, max_size=10))
    def test_any_reciprocal_matrix_gives_valid_weights_and_cr_gate(self, upper):
        m = np.ones((5, 5))
        pairs = [(r, c) for r in range(5) for c in range(r + 1, 5)]
        for v, (i, j) in zip(upper, pairs, strict=True):
            m[i, j], m[j, i] = v, 1 / v
        res = calculate_ahp(m)
        got = np.array(list(res.weights.values()))
        self.assertAlmostEqual(got.sum(), 1.0, places=9)
        self.assertTrue((got >= 0).all())
        self.assertGreaterEqual(res.cr, 0.0)
        if res.cr >= 0.1:
            with self.assertRaises(ValueError):
                calculate_ahp(m, raise_on_inconsistent=True)
