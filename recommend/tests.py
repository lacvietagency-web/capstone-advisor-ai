"""Kiểm thử cho module recommend:

1. EngineTests: kiểm thử công thức M1–M3 và lọc cứng.
2. AHPTests: kiểm thử tính toán AHP, kiểm định CR, WeightSet model, lệnh ahp_weights và file mẫu ahp_mau.json.
"""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock

from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from accounts.models import User
from catalog.models import (
    Course,
    Field,
    Lecturer,
    Major,
    Skill,
    Student,
    StudentCourseResult,
    StudentInterest,
    StudentSkill,
    Topic,
    TopicPrerequisite,
    TopicSkill,
)
from recommend.admin import WeightSetAdmin
from recommend.ahp import (
    CRITERIA,
    calculate_ahp,
    calculate_ahp_geometric,
    compute_ahp,
)
from recommend.engine import (
    DEFAULT_WEIGHTS,
    Profile,
    eligible,
    get_active_weights,
    get_active_weights_version,
    m1_skill,
    m2_academic,
    m3_field,
    score_student,
)
from recommend.models import WeightSet


class EngineTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        web = Field.objects.create(name="Web")
        Field.objects.create(name="AI")
        java, sql, py = (Skill.objects.create(name=n) for n in ("Java", "SQL", "Python"))
        cls.db = Course.objects.create(code="DB", name="Cơ sở dữ liệu", field=web)
        lec = Lecturer.objects.create(user=User.objects.create_user("gv", role="LECTURER"))
        st = Student.objects.create(
            user=User.objects.create_user("sv"), student_code="1", major=Major.objects.create(name="CNTT"), gpa=3.2
        )
        StudentSkill.objects.create(student=st, skill=java, level=4)
        StudentSkill.objects.create(student=st, skill=sql, level=2)
        StudentInterest.objects.create(student=st, field=web, level=3)
        StudentCourseResult.objects.create(student=st, course=cls.db, score=8)
        t = Topic.objects.create(lecturer=lec, title="Web bán hàng", description="Spring Boot, MySQL", min_gpa=2.5)
        t.fields.set([web])
        TopicSkill.objects.create(topic=t, skill=java, required_level=3)  # đạt: min(4/3,1)=1
        TopicSkill.objects.create(topic=t, skill=sql, required_level=4)  # một nửa: 2/4 = 0.5
        TopicPrerequisite.objects.create(topic=t, course=cls.db, min_score=5)
        cls.st, cls.t, cls.py = st, t, py

    def test_m1_skill(self):
        score, missing = m1_skill(Profile(self.st), self.t)
        self.assertAlmostEqual(score, 75.0)  # (1 + 0.5) / 2
        self.assertEqual(missing, ["SQL"])

    def test_m2_academic(self):
        self.assertAlmostEqual(m2_academic(Profile(self.st), self.t), 100 * (0.4 * 3.2 / 4 + 0.6 * 8 / 10))  # 80.0

    def test_m3_field(self):
        self.assertAlmostEqual(m3_field(Profile(self.st), self.t), 100.0)  # SV quan tâm Web mức 3/3

    def test_hard_filter_gpa_and_mandatory_skill(self):
        self.assertTrue(eligible(Profile(self.st), self.t)[0])
        TopicSkill.objects.create(topic=self.t, skill=self.py, required_level=3, is_mandatory=True)
        ok, why = eligible(Profile(self.st), self.t)
        self.assertFalse(ok)
        self.assertIn("Python", why)

    def test_ranking_runs(self):
        self.assertEqual(score_student(self.st, semantic=False)[0].topic, self.t)


class AHPTests(TestCase):
    """Kiểm thử đặc tả AHP: tính trọng số, kiểm tra tính nhất quán, model WeightSet và lệnh ahp_weights."""

    def setUp(self):
        # Ma trận nhất quán hoàn hảo từ tỉ lệ mong đợi [0.25, 0.20, 0.15, 0.20, 0.20]
        # a_ij = w_i / w_j
        self.target_weights = [0.25, 0.20, 0.15, 0.20, 0.20]
        self.perfect_matrix = [[w_i / w_j for w_j in self.target_weights] for w_i in self.target_weights]

        # Ma trận thiếu nhất quán với các so sánh mâu thuẫn (CR >= 0.1)
        self.inconsistent_matrix = [
            [1.0, 5.0, 1.0 / 5.0, 7.0, 1.0 / 3.0],
            [1.0 / 5.0, 1.0, 4.0, 1.0 / 6.0, 3.0],
            [5.0, 1.0 / 4.0, 1.0, 1.0 / 2.0, 6.0],
            [1.0 / 7.0, 6.0, 2.0, 1.0, 1.0 / 4.0],
            [3.0, 1.0 / 3.0, 1.0 / 6.0, 4.0, 1.0],
        ]

    def test_perfect_consistency_eigen_method(self):
        """Ma trận nhất quán hoàn hảo → CR ≈ 0 và trọng số đúng tỉ lệ theo phương pháp trị riêng."""
        result = calculate_ahp(self.perfect_matrix)
        self.assertLess(result.cr, 1e-4)
        self.assertTrue(result.is_consistent)
        self.assertAlmostEqual(result.lambda_max, 5.0, places=4)
        self.assertAlmostEqual(result.ci, 0.0, places=4)

        for criterion, expected_w in zip(CRITERIA, self.target_weights, strict=True):
            self.assertAlmostEqual(result.weights[criterion], expected_w, places=4)

        # Kiểm tra tính chuẩn hoá: tổng trọng số = 1
        self.assertAlmostEqual(sum(result.weights.values()), 1.0, places=4)

    def test_perfect_consistency_geometric_method(self):
        """Ma trận nhất quán hoàn hảo → CR ≈ 0 và trọng số đúng tỉ lệ theo trung bình hình học."""
        result = calculate_ahp_geometric(self.perfect_matrix)
        self.assertLess(result.cr, 1e-4)
        self.assertTrue(result.is_consistent)
        self.assertAlmostEqual(result.lambda_max, 5.0, places=4)

        for criterion, expected_w in zip(CRITERIA, self.target_weights, strict=True):
            self.assertAlmostEqual(result.weights[criterion], expected_w, places=4)

    def test_compute_ahp_alias(self):
        """compute_ahp là alias của calculate_ahp."""
        res1 = calculate_ahp(self.perfect_matrix)
        res2 = compute_ahp(self.perfect_matrix)
        self.assertEqual(res1.weights, res2.weights)
        self.assertEqual(res1.cr, res2.cr)

    def test_inconsistent_matrix_detected(self):
        """Ma trận thiếu nhất quán có CR >= 0.1 và bị phát hiện đúng."""
        result = calculate_ahp(self.inconsistent_matrix)
        self.assertGreaterEqual(result.cr, 0.1)
        self.assertFalse(result.is_consistent)

        with self.assertRaises(ValueError):
            calculate_ahp(self.inconsistent_matrix, raise_on_inconsistent=True)

    def test_inconsistent_matrix_rejected_by_model(self):
        """Model WeightSet từ chối ma trận thiếu nhất quán khi CR >= 0.1."""
        ws = WeightSet(
            name="Bộ không nhất quán",
            weights=DEFAULT_WEIGHTS,
            matrix=self.inconsistent_matrix,
            cr=0.25,
        )
        with self.assertRaises(ValidationError):
            ws.clean()

        with self.assertRaises(ValueError):
            WeightSet.from_matrix(name="Bộ lỗi", matrix=self.inconsistent_matrix)

    def test_inconsistent_matrix_rejected_by_command(self):
        """Lệnh ahp_weights từ chối ma trận có CR >= 0.1."""
        with NamedTemporaryFile("w+", suffix=".json") as f:
            json.dump(self.inconsistent_matrix, f)
            f.flush()
            with self.assertRaises(CommandError) as ctx:
                call_command("ahp_weights", matrix=f.name, name="Thử nghiệm lỗi")
            self.assertIn("CR =", str(ctx.exception))
            self.assertIn("bị từ chối", str(ctx.exception))

    def test_ahp_mau_json_exists_and_valid(self):
        """File mẫu recommend/ahp_mau.json tồn tại, hợp lệ và có CR < 0.1."""
        mau_path = Path(__file__).resolve().parent / "ahp_mau.json"
        self.assertTrue(mau_path.exists(), "File recommend/ahp_mau.json phải tồn tại.")

        with open(mau_path, encoding="utf-8") as f:
            data = json.load(f)

        result = calculate_ahp(data)
        self.assertLess(result.cr, 0.1, "Ma trận mẫu của chuyên gia phải đạt CR < 0.1.")
        self.assertTrue(result.is_consistent)

        # Chạy lệnh ahp_weights với file mẫu
        call_command("ahp_weights", matrix=str(mau_path), name="Chuyên gia mẫu v1", active=True)
        ws = WeightSet.objects.get(name="Chuyên gia mẫu v1")
        self.assertTrue(ws.is_active)
        self.assertLess(ws.cr, 0.1)
        self.assertEqual(len(ws.weights), 5)
        for c in CRITERIA:
            self.assertIn(c, ws.weights)

    def test_weightset_single_active(self):
        """Chỉ có duy nhất một bộ trọng số được is_active=True tại một thời điểm."""
        ws1 = WeightSet.objects.create(name="Bộ 1", weights=DEFAULT_WEIGHTS, matrix=[], cr=0.02, is_active=True)
        ws2 = WeightSet.objects.create(name="Bộ 2", weights=DEFAULT_WEIGHTS, matrix=[], cr=0.03, is_active=True)

        ws1.refresh_from_db()
        ws2.refresh_from_db()
        self.assertFalse(ws1.is_active)
        self.assertTrue(ws2.is_active)

    def test_engine_uses_active_weights(self):
        """Engine lấy bộ trọng số is_active; nếu không có thì fallback về DEFAULT_WEIGHTS."""
        WeightSet.objects.all().delete()
        self.assertEqual(get_active_weights(), DEFAULT_WEIGHTS)
        self.assertEqual(get_active_weights_version(), "expert-v0")

        custom_w = {"skill": 0.40, "academic": 0.20, "field": 0.20, "semantic": 0.10, "llm": 0.10}
        WeightSet.objects.create(name="Tùy biến Khoa", weights=custom_w, matrix=[], cr=0.01, is_active=True)

        self.assertEqual(get_active_weights(), custom_w)
        self.assertEqual(get_active_weights_version(), "Tùy biến Khoa")

    def test_admin_activate_action(self):
        """Action trong Admin cho phép Khoa chọn kích hoạt một bộ trọng số."""
        admin = WeightSetAdmin(WeightSet, AdminSite())
        ws1 = WeightSet.objects.create(name="B1", weights=DEFAULT_WEIGHTS, matrix=[], cr=0.01, is_active=True)
        ws2 = WeightSet.objects.create(name="B2", weights=DEFAULT_WEIGHTS, matrix=[], cr=0.01, is_active=False)

        request = MagicMock()
        admin.activate_weight_set(request, WeightSet.objects.filter(pk=ws2.pk))

        ws1.refresh_from_db()
        ws2.refresh_from_db()
        self.assertFalse(ws1.is_active)
        self.assertTrue(ws2.is_active)

    def test_weightset_str(self):
        """Kiểm tra phương thức __str__ của WeightSet."""
        ws = WeightSet(name="Bộ thử", weights=DEFAULT_WEIGHTS, matrix=[], cr=0.0456, is_active=True)
        self.assertIn("Bộ thử", str(ws))
        self.assertIn("0.0456", str(ws))
        self.assertIn("[Đang dùng]", str(ws))
