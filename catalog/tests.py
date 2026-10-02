from django.core.management import call_command
from django.test import TestCase, override_settings

from catalog.models import Field, Preference, Skill, Topic


@override_settings(RECOMMEND_SEMANTIC=False)
class BusinessFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=6, verbosity=0)

    def login(self, user):
        self.client.login(username=user, password="123456")

    def test_student_preferences_no_duplicates(self):
        self.login("sv001")
        t1, t2 = Topic.objects.all()[:2]
        r = self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t1.pk})
        self.assertContains(r, "không được trùng")
        self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t2.pk})
        self.assertEqual(
            list(
                Preference.objects.filter(student__user__username="sv001")
                .order_by("rank")
                .values_list("topic_id", flat=True)
            ),
            [t1.pk, t2.pk],
        )

    def test_student_profile_save_recomputes(self):
        self.login("sv001")
        r = self.client.get("/ho-so/")
        self.assertEqual(r.status_code, 200)

    def test_lecturer_creates_topic(self):
        self.login("gv001")
        f = Field.objects.first()
        sk = Skill.objects.first()
        r = self.client.post(
            "/de-tai/them/",
            {
                "title": "Đề tài mới",
                "description": "Mô tả",
                "fields": [f.pk],
                "difficulty": 2,
                "min_gpa": "2.0",
                "capacity": 1,
                "status": "OPEN",
                "skills-TOTAL_FORMS": 1,
                "skills-INITIAL_FORMS": 0,
                "skills-0-skill": sk.pk,
                "skills-0-required_level": 3,
                "skills-0-weight": 1,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Topic.objects.filter(title="Đề tài mới", skills__skill=sk).exists())

    def test_roles_are_separated(self):
        self.login("sv001")
        self.assertEqual(self.client.get("/de-tai/").status_code, 403)
        self.client.logout()
        self.login("gv001")
        self.assertEqual(self.client.get("/nguyen-vong/").status_code, 403)
