"""Kiểm thử công thức M1–M3 và lọc cứng trên một ví dụ tính tay được."""
from django.test import TestCase

from accounts.models import User
from catalog.models import (Course, Field, Lecturer, Major, Skill, Student, StudentCourseResult, StudentInterest,
                            StudentSkill, Topic, TopicPrerequisite, TopicSkill)
from recommend.engine import Profile, eligible, m1_skill, m2_academic, m3_field, score_student


class EngineTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        web, ai = Field.objects.create(name="Web"), Field.objects.create(name="AI")
        java, sql, py = (Skill.objects.create(name=n) for n in ("Java", "SQL", "Python"))
        cls.db = Course.objects.create(code="DB", name="Cơ sở dữ liệu", field=web)
        lec = Lecturer.objects.create(user=User.objects.create_user("gv", role="LECTURER"))
        st = Student.objects.create(user=User.objects.create_user("sv"), student_code="1", major=Major.objects.create(name="CNTT"), gpa=3.2)
        StudentSkill.objects.create(student=st, skill=java, level=4)
        StudentSkill.objects.create(student=st, skill=sql, level=2)
        StudentInterest.objects.create(student=st, field=web, level=3)
        StudentCourseResult.objects.create(student=st, course=cls.db, score=8)
        t = Topic.objects.create(lecturer=lec, title="Web bán hàng", description="Spring Boot, MySQL", min_gpa=2.5)
        t.fields.set([web])
        TopicSkill.objects.create(topic=t, skill=java, required_level=3)          # đạt: min(4/3,1)=1
        TopicSkill.objects.create(topic=t, skill=sql, required_level=4)           # một nửa: 2/4 = 0.5
        TopicPrerequisite.objects.create(topic=t, course=cls.db, min_score=5)
        cls.st, cls.t, cls.py = st, t, py

    def test_m1_skill(self):
        score, missing = m1_skill(Profile(self.st), self.t)
        self.assertAlmostEqual(score, 75.0)                 # (1 + 0.5) / 2
        self.assertEqual(missing, ["SQL"])

    def test_m2_academic(self):
        self.assertAlmostEqual(m2_academic(Profile(self.st), self.t), 100 * (0.4 * 3.2 / 4 + 0.6 * 8 / 10))   # 80.0

    def test_m3_field(self):
        self.assertAlmostEqual(m3_field(Profile(self.st), self.t), 100.0)   # SV quan tâm Web mức 3/3

    def test_hard_filter_gpa_and_mandatory_skill(self):
        self.assertTrue(eligible(Profile(self.st), self.t)[0])
        TopicSkill.objects.create(topic=self.t, skill=self.py, required_level=3, is_mandatory=True)
        ok, why = eligible(Profile(self.st), self.t)
        self.assertFalse(ok); self.assertIn("Python", why)

    def test_ranking_runs(self):
        self.assertEqual(score_student(self.st, semantic=False)[0].topic, self.t)
