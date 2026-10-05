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

READY = all(
    hasattr(solver, f) for f in ("solve_ilp", "solve_greedy", "metrics")
)  # chưa có lời giải → bỏ qua, không làm đỏ CI
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
        d = base(
            prefs={"s1": ["A", "B"], "s2": ["A", "B"]},
            scores={("s1", "A"): 90, ("s2", "A"): 60, ("s1", "B"): 70, ("s2", "B"): 70},
            cap={"A": 1, "B": 1},
            owner={"A": "g1", "B": "g2"},
            quota={"g1": 5, "g2": 5},
            gpa={"s1": 3, "s2": 3},
        )
        a = solve_ilp(**d)
        self.assertEqual(a, {"s1": "A", "s2": "B"})

    def test_ilp_beats_greedy_on_coverage(self):
        """Ca kinh điển: Greedy xếp s1 (điểm cao) vào A → s2 (chỉ chọn A) trắng tay. ILP đẩy s1 sang B để xếp đủ cả hai."""
        d = base(
            prefs={"s1": ["A", "B"], "s2": ["A"]},
            scores={("s1", "A"): 95, ("s1", "B"): 80, ("s2", "A"): 70},
            cap={"A": 1, "B": 1},
            owner={"A": "g1", "B": "g1"},
            quota={"g1": 5},
            gpa={"s1": 3.5, "s2": 3.0},
        )
        self.assertIsNone(solve_greedy(**d)["s2"])
        self.assertEqual(solve_ilp(**d), {"s1": "B", "s2": "A"})

    def test_lecturer_quota_respected(self):
        d = base(
            prefs={f"s{i}": ["A", "B"] for i in range(4)},
            scores={(f"s{i}", t): 50 for i in range(4) for t in "AB"},
            cap={"A": 3, "B": 3},
            owner={"A": "g1", "B": "g1"},
            quota={"g1": 2},
            gpa={f"s{i}": 3 for i in range(4)},
        )
        a = solve_ilp(**d)
        self.assertEqual(sum(1 for t in a.values() if t), 2)
        self.assertEqual(metrics(a, d["prefs"], d["scores"], d["cap"], d["owner"], d["quota"])["quota_violations"], 0)

    def test_never_outside_preferences(self):
        d = base(
            prefs={"s1": ["A"], "s2": ["A"]},
            scores={("s1", "A"): 80, ("s2", "A"): 70, ("s1", "C"): 99, ("s2", "C"): 99},
            cap={"A": 1, "C": 5},
            owner={"A": "g1", "C": "g1"},
            quota={"g1": 10},
            gpa={"s1": 3, "s2": 3},
        )
        a = solve_ilp(**d)
        for s, t in a.items():
            self.assertTrue(t is None or t in d["prefs"][s])
        self.assertEqual(sorted(a.values(), key=str), ["A", None])

    def test_tie_break_by_gpa(self):
        d = base(
            prefs={"s1": ["A"], "s2": ["A"]},
            scores={("s1", "A"): 70, ("s2", "A"): 70},
            cap={"A": 1},
            owner={"A": "g1"},
            quota={"g1": 5},
            gpa={"s1": 2.5, "s2": 3.6},
        )
        self.assertEqual(solve_ilp(**d), {"s1": None, "s2": "A"})

    def test_metrics(self):
        prefs = {"s1": ["A", "B"], "s2": ["A", "B"], "s3": ["C"]}
        scores = {("s1", "A"): 80, ("s2", "B"): 60}
        m = metrics(
            {"s1": "A", "s2": "B", "s3": None},
            prefs,
            scores,
            {"A": 1, "B": 1, "C": 1},
            {"A": "g", "B": "g", "C": "g"},
            {"g": 5},
        )
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


@override_settings(RECOMMEND_SEMANTIC=False)
class AllocationFlowTests(TestCase):
    def setUp(self):
        from accounts.models import User
        from catalog.models import Lecturer, RegistrationPeriod, Student

        call_command("seed_demo", students=10, lecturers=3, topics=8, verbosity=0)
        call_command("recommend_all", verbosity=0)

        self.period = RegistrationPeriod.objects.first()
        self.admin_user = User.objects.create_user(username="admin_khoa", password="password123", role=User.Role.ADMIN)
        self.student_user = Student.objects.first().user
        self.lecturer_user = Lecturer.objects.first().user

    def test_access_permissions(self):
        """Khách và người dùng không phải Khoa bị từ chối truy cập."""
        # Khách vãng lai
        res = self.client.get("/khoa/phan-cong/")
        self.assertEqual(res.status_code, 302)

        # Sinh viên -> 403 Forbidden
        self.client.force_login(self.student_user)
        res = self.client.get("/khoa/phan-cong/")
        self.assertEqual(res.status_code, 403)

        # Giảng viên -> 403 Forbidden
        self.client.force_login(self.lecturer_user)
        res = self.client.get("/khoa/phan-cong/")
        self.assertEqual(res.status_code, 403)

        # Khoa (Admin) -> 200 OK
        self.client.force_login(self.admin_user)
        res = self.client.get("/khoa/phan-cong/")
        self.assertEqual(res.status_code, 200)

    def test_run_ilp_and_greedy_flow(self):
        """Khoa chạy phân công ILP và Greedy qua giao diện, ghi nhận AuditLog."""
        from allocate.models import Allocation
        from catalog.models import AuditLog, RegistrationPeriod

        self.client.force_login(self.admin_user)

        # Chạy ILP
        res = self.client.post("/khoa/phan-cong/", {"action": "run_ilp", "period_id": self.period.pk})
        self.assertRedirects(res, f"/khoa/phan-cong/?period_id={self.period.pk}")

        self.period.refresh_from_db()
        self.assertEqual(self.period.status, RegistrationPeriod.Status.OPTIMIZED)
        self.assertEqual(Allocation.objects.filter(period=self.period).count(), 10)
        self.assertTrue(
            all(
                a.status == Allocation.Status.DRAFT and a.source == Allocation.Source.ILP
                for a in Allocation.objects.all()
            )
        )
        self.assertTrue(
            AuditLog.objects.filter(user=self.admin_user, action="run_allocation", entity="RegistrationPeriod").exists()
        )

        # Chạy Greedy
        res = self.client.post("/khoa/phan-cong/", {"action": "run_greedy", "period_id": self.period.pk})
        self.assertRedirects(res, f"/khoa/phan-cong/?period_id={self.period.pk}")
        self.assertTrue(
            all(
                a.status == Allocation.Status.DRAFT and a.source == Allocation.Source.GREEDY
                for a in Allocation.objects.all()
            )
        )

    def test_filter_unassigned_and_metrics_display(self):
        """Kiểm tra chức năng lọc danh sách chưa xếp và hiển thị số liệu metrics."""
        from allocate.models import Allocation
        from allocate.services import run_allocation

        run_allocation(self.period, algorithm="ILP")

        # Đặt 1 sinh viên thành chưa xếp để kiểm tra bộ lọc
        alloc = Allocation.objects.filter(period=self.period).first()
        alloc.topic = None
        alloc.preference_rank = None
        alloc.match_score = None
        alloc.save()

        self.client.force_login(self.admin_user)
        res = self.client.get(f"/khoa/phan-cong/?period_id={self.period.pk}&unassigned_only=1")
        self.assertEqual(res.status_code, 200)
        expected_unassigned = Allocation.objects.filter(period=self.period, topic__isnull=True).count()
        self.assertEqual(len(res.context["allocations"]), expected_unassigned)
        self.assertTrue(all(a.topic is None for a in res.context["allocations"]))
        self.assertIsNotNone(res.context["metrics"])
        self.assertIn("Tỉ lệ phân công", res.content.decode("utf-8"))

    def test_phase2_suggestions_and_manual_assign(self):
        """Pha 2: Gợi ý đề tài cho SV chưa xếp và Khoa chỉnh tay (source=MANUAL)."""
        from allocate.models import Allocation
        from allocate.services import run_allocation
        from catalog.models import AuditLog, Topic

        run_allocation(self.period, algorithm="ILP")

        # Lấy 1 sinh viên và đưa về trạng thái chưa xếp
        unassigned_alloc = Allocation.objects.filter(period=self.period).first()
        st = unassigned_alloc.student
        unassigned_alloc.topic = None
        unassigned_alloc.save()

        self.client.force_login(self.admin_user)
        # Xem gợi ý Pha 2
        res = self.client.get(f"/khoa/phan-cong/?period_id={self.period.pk}&suggest_student_id={st.pk}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["suggest_student"], st)
        suggestions = res.context["suggestions"]
        self.assertIsInstance(suggestions, list)
        if len(suggestions) > 1:
            self.assertGreaterEqual(suggestions[0]["score"], suggestions[1]["score"])

        # Khoa chọn tay đề tài
        chosen_topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        post_res = self.client.post(
            "/khoa/phan-cong/",
            {
                "action": "manual_assign",
                "student_id": st.pk,
                "topic_id": chosen_topic.pk,
            },
        )
        self.assertRedirects(post_res, f"/khoa/phan-cong/?period_id={self.period.pk}")

        unassigned_alloc.refresh_from_db()
        self.assertEqual(unassigned_alloc.topic, chosen_topic)
        self.assertEqual(unassigned_alloc.source, Allocation.Source.MANUAL)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin_user, action="manual_assign", entity="Allocation", entity_id=str(unassigned_alloc.pk)
            ).exists()
        )

    def test_publish_allocations_flow(self):
        """Nút Chốt chuyển DRAFT->OFFICIAL, đợt->PUBLISHED và ghi AuditLog."""
        from allocate.models import Allocation
        from allocate.services import run_allocation
        from catalog.models import AuditLog, RegistrationPeriod

        run_allocation(self.period, algorithm="ILP")

        self.client.force_login(self.admin_user)
        res = self.client.post("/khoa/phan-cong/", {"action": "publish", "period_id": self.period.pk})
        self.assertRedirects(res, f"/khoa/phan-cong/?period_id={self.period.pk}")

        self.period.refresh_from_db()
        self.assertEqual(self.period.status, RegistrationPeriod.Status.PUBLISHED)
        self.assertTrue(
            all(a.status == Allocation.Status.OFFICIAL for a in Allocation.objects.filter(period=self.period))
        )
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin_user, action="publish_allocations", entity="RegistrationPeriod"
            ).exists()
        )

    def test_allocate_period_greedy_saves_drafts(self):
        from allocate.models import Allocation

        call_command("seed_demo", students=20, lecturers=4, topics=10, verbosity=0)
        call_command("recommend_all", verbosity=0)
        call_command("allocate_period", algorithm="GREEDY", verbosity=0)
        self.assertEqual(Allocation.objects.count(), 20)
        self.assertTrue(all(a.status == "DRAFT" and a.source == "GREEDY" for a in Allocation.objects.all()))

    def test_rejected_preference_not_allocated_ilp(self):
        """[UC12] Kiểm thử: SV bị từ chối không được xếp vào đề tài đó khi chạy ILP."""
        from allocate.models import Allocation
        from catalog.models import Preference

        call_command("seed_demo", students=10, lecturers=3, topics=5, verbosity=0)
        call_command("recommend_all", verbosity=0)
        call_command("allocate_period", algorithm="ILP", verbosity=0)

        assigned_alloc = Allocation.objects.filter(topic__isnull=False).first()
        self.assertIsNotNone(assigned_alloc)
        st = assigned_alloc.student
        tp = assigned_alloc.topic

        # Đánh dấu từ chối nguyện vọng này
        Preference.objects.filter(student=st, topic=tp).update(status=Preference.Status.REJECTED)

        # Chạy lại ILP
        call_command("allocate_period", algorithm="ILP", verbosity=0)
        new_alloc = Allocation.objects.get(student=st)
        self.assertNotEqual(new_alloc.topic, tp, "Sinh viên bị từ chối không được xếp vào đề tài đó")

    def test_rejected_preference_not_allocated_greedy(self):
        """[UC12] Kiểm thử: SV bị từ chối không được xếp vào đề tài đó khi chạy GREEDY."""
        from allocate.models import Allocation
        from catalog.models import Preference

        call_command("seed_demo", students=10, lecturers=3, topics=5, verbosity=0)
        call_command("recommend_all", verbosity=0)
        call_command("allocate_period", algorithm="GREEDY", verbosity=0)

        assigned_alloc = Allocation.objects.filter(topic__isnull=False).first()
        self.assertIsNotNone(assigned_alloc)
        st = assigned_alloc.student
        tp = assigned_alloc.topic

        # Đánh dấu từ chối nguyện vọng này
        Preference.objects.filter(student=st, topic=tp).update(status=Preference.Status.REJECTED)

        # Chạy lại GREEDY
        call_command("allocate_period", algorithm="GREEDY", verbosity=0)
        new_alloc = Allocation.objects.get(student=st)
        self.assertNotEqual(new_alloc.topic, tp, "Sinh viên bị từ chối không được xếp vào đề tài đó")

    def test_all_preferences_rejected_results_in_unassigned(self):
        """[UC12] Sinh viên bị từ chối tất cả nguyện vọng thì không được xếp đề tài (topic=None)."""
        from allocate.models import Allocation
        from catalog.models import Preference

        call_command("seed_demo", students=10, lecturers=3, topics=5, verbosity=0)
        call_command("recommend_all", verbosity=0)

        pref = Preference.objects.first()
        self.assertIsNotNone(pref)
        st = pref.student

        # Từ chối toàn bộ nguyện vọng của sinh viên này
        Preference.objects.filter(student=st).update(status=Preference.Status.REJECTED)

        call_command("allocate_period", algorithm="ILP", verbosity=0)
        new_alloc = Allocation.objects.get(student=st)
        self.assertIsNone(new_alloc.topic)
        self.assertIsNone(new_alloc.preference_rank)


@override_settings(RECOMMEND_SEMANTIC=False)
class StudentAllocationResultTests(TestCase):
    """[UC08] Kiểm thử sinh viên xem kết quả phân công đồ án tốt nghiệp."""

    def setUp(self):
        from django.utils import timezone

        from accounts.models import User
        from catalog.models import Field, Lecturer, Major, RegistrationPeriod, Skill, Student, Topic

        self.major = Major.objects.create(name="Công nghệ thông tin")
        self.field = Field.objects.create(name="Trí tuệ nhân tạo")
        self.skill = Skill.objects.create(name="Python", field=self.field)

        # Tạo tài khoản sinh viên
        self.u_sv = User.objects.create_user(username="sv_test", password="password123", role=User.Role.STUDENT)
        self.student = Student.objects.create(
            user=self.u_sv, student_code="SV001", major=self.major, gpa=3.6, about="SV chuyên cần"
        )

        # Tạo tài khoản giảng viên
        self.u_gv = User.objects.create_user(
            username="gv_test", password="password123", role=User.Role.LECTURER, first_name="A", last_name="Nguyễn Văn"
        )
        self.lecturer = Lecturer.objects.create(user=self.u_gv, department="Bộ môn Khoa học máy tính", max_students=5)

        # Tạo đề tài
        self.topic = Topic.objects.create(
            lecturer=self.lecturer,
            title="Nghiên cứu ứng dụng Học máy trong phân loại văn bản",
            description="Mô tả đề tài chi tiết...",
            capacity=1,
            status=Topic.Status.OPEN,
        )
        self.topic.fields.add(self.field)

        # Tạo tài khoản khoa / admin
        self.u_admin = User.objects.create_user(username="admin_test", password="password123", role=User.Role.ADMIN)

        # Đợt đăng ký
        now = timezone.now()
        self.period = RegistrationPeriod.objects.create(
            name="Đợt 1 - 2026",
            start_at=now,
            end_at=now + timezone.timedelta(days=30),
            status=RegistrationPeriod.Status.OPEN,
        )

    def test_access_permissions(self):
        """Khách vãng lai bị chuyển hướng đăng nhập; GV và Khoa bị 403; SV vào được."""
        # Khách vãng lai
        res = self.client.get("/ket-qua/")
        self.assertEqual(res.status_code, 302)

        # Giảng viên -> 403 Forbidden
        self.client.force_login(self.u_gv)
        res = self.client.get("/ket-qua/")
        self.assertEqual(res.status_code, 403)

        # Admin Khoa -> 403 Forbidden
        self.client.force_login(self.u_admin)
        res = self.client.get("/ket-qua/")
        self.assertEqual(res.status_code, 403)

        # Sinh viên -> 200 OK
        self.client.force_login(self.u_sv)
        res = self.client.get("/ket-qua/")
        self.assertEqual(res.status_code, 200)

    def test_when_period_not_published_shows_waiting_status(self):
        """Khi đợt chưa công bố (status != PUBLISHED): trang chủ SV và /ket-qua/ hiện trạng thái chờ."""
        from allocate.models import Allocation

        # Giả lập đã có bản ghi Allocation dạng DRAFT
        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=self.topic,
            preference_rank=1,
            match_score=92.5,
            status=Allocation.Status.DRAFT,
        )

        self.client.force_login(self.u_sv)

        # Kiểm tra trang /ket-qua/
        res_kq = self.client.get("/ket-qua/")
        self.assertEqual(res_kq.status_code, 200)
        self.assertFalse(res_kq.context["is_published"])
        content_kq = res_kq.content.decode("utf-8")
        self.assertIn("Hội đồng Khoa đang thẩm định phân công", content_kq)
        # Kết quả nháp tuyệt đối không được công bố
        self.assertNotIn("Chúc mừng bạn đã được phân công", content_kq)

        # Kiểm tra trang chủ /trang-chu/
        res_home = self.client.get("/trang-chu/")
        self.assertEqual(res_home.status_code, 200)
        content_home = res_home.content.decode("utf-8")
        self.assertIn("Hội đồng Khoa đang thẩm định phân công", content_home)
        self.assertNotIn("Chúc mừng bạn đã được phân công", content_home)

    def test_when_period_published_shows_assigned_details(self):
        """Khi đợt PUBLISHED: trang chủ SV và /ket-qua/ hiện đề tài được phân, GVHD, NV đạt, điểm phù hợp."""
        from allocate.models import Allocation
        from catalog.models import RegistrationPeriod

        self.period.status = RegistrationPeriod.Status.PUBLISHED
        self.period.save()

        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=self.topic,
            preference_rank=1,
            match_score=88.5,
            status=Allocation.Status.OFFICIAL,
        )

        self.client.force_login(self.u_sv)

        # 1. Kiểm tra màn hình /ket-qua/
        res_kq = self.client.get("/ket-qua/")
        self.assertEqual(res_kq.status_code, 200)
        self.assertTrue(res_kq.context["is_published"])
        self.assertEqual(res_kq.context["topic"], self.topic)
        self.assertEqual(res_kq.context["preference_rank"], 1)
        self.assertEqual(res_kq.context["match_score"], 88.5)

        content_kq = res_kq.content.decode("utf-8")
        self.assertIn("Đề tài được phân", content_kq)
        self.assertIn(self.topic.title, content_kq)
        self.assertIn("GVHD", content_kq)
        self.assertIn("Nguyễn Văn A", content_kq)
        self.assertIn("NV đạt", content_kq)
        self.assertIn("NV1", content_kq)
        self.assertIn("Điểm phù hợp", content_kq)
        self.assertTrue("88,5" in content_kq or "88.5" in content_kq)

        # 2. Kiểm tra trang chủ sinh viên
        res_home = self.client.get("/trang-chu/")
        self.assertEqual(res_home.status_code, 200)
        content_home = res_home.content.decode("utf-8")
        self.assertIn("Đề tài được phân", content_home)
        self.assertIn(self.topic.title, content_home)
        self.assertIn("GVHD", content_home)
        self.assertIn("Nguyễn Văn A", content_home)
        self.assertIn("NV đạt", content_home)
        self.assertIn("NV1", content_home)
        self.assertIn("Điểm phù hợp", content_home)
        self.assertTrue("88,5" in content_home or "88.5" in content_home)

    def test_when_period_published_but_student_unassigned(self):
        """Khi đợt PUBLISHED nhưng sinh viên chưa được xếp: hiện thông báo chưa phân công."""
        from allocate.models import Allocation
        from catalog.models import RegistrationPeriod

        self.period.status = RegistrationPeriod.Status.PUBLISHED
        self.period.save()

        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=None,
            preference_rank=None,
            match_score=None,
            status=Allocation.Status.OFFICIAL,
        )

        self.client.force_login(self.u_sv)

        res_kq = self.client.get("/ket-qua/")
        self.assertEqual(res_kq.status_code, 200)
        self.assertTrue(res_kq.context["is_published"])
        self.assertTrue(res_kq.context["unassigned"])
        content_kq = res_kq.content.decode("utf-8")
        self.assertIn("Chưa được phân công đề tài", content_kq)

        res_home = self.client.get("/trang-chu/")
        self.assertEqual(res_home.status_code, 200)
        content_home = res_home.content.decode("utf-8")
        self.assertIn("Bạn hiện chưa được phân công đề tài", content_home)

    def test_filter_by_period_id(self):
        """Sinh viên có thể chọn xem kết quả giữa các đợt khác nhau qua query param period_id."""
        from django.utils import timezone

        from allocate.models import Allocation
        from catalog.models import RegistrationPeriod

        # Đợt 1 đã công bố
        self.period.status = RegistrationPeriod.Status.PUBLISHED
        self.period.save()
        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=self.topic,
            preference_rank=2,
            match_score=75.0,
            status=Allocation.Status.OFFICIAL,
        )

        # Đợt 2 mới mở, chưa công bố
        now = timezone.now() + timezone.timedelta(days=60)
        period2 = RegistrationPeriod.objects.create(
            name="Đợt 2 - 2026",
            start_at=now,
            end_at=now + timezone.timedelta(days=30),
            status=RegistrationPeriod.Status.OPEN,
        )

        self.client.force_login(self.u_sv)

        # Xem đợt 1 -> hiển thị kết quả chính thức
        r1 = self.client.get(f"/ket-qua/?period_id={self.period.pk}")
        self.assertEqual(r1.status_code, 200)
        self.assertTrue(r1.context["is_published"])
        self.assertEqual(r1.context["preference_rank"], 2)

        # Xem đợt 2 -> hiển thị trạng thái chờ
        r2 = self.client.get(f"/ket-qua/?period_id={period2.pk}")
        self.assertEqual(r2.status_code, 200)
        self.assertFalse(r2.context["is_published"])
        self.assertIn("Hội đồng Khoa đang thẩm định phân công", r2.content.decode("utf-8"))

    def test_service_when_no_period_exists(self):
        """Khi hệ thống chưa có đợt nào, service trả về is_published=False và period=None."""
        from allocate.services import get_student_allocation_result
        from catalog.models import RegistrationPeriod

        RegistrationPeriod.objects.all().delete()
        res = get_student_allocation_result(self.student)
        self.assertFalse(res["is_published"])
        self.assertIsNone(res["period"])
        self.assertIn("Chưa có đợt đăng ký nào", res["status_text"])

    def test_service_score_fallback_to_recommendation(self):
        """Nếu Allocation chưa lưu điểm thì tự động lấy điểm từ bảng Recommendation."""
        from allocate.models import Allocation
        from allocate.services import get_student_allocation_result
        from catalog.models import RegistrationPeriod
        from recommend.models import Recommendation

        self.period.status = RegistrationPeriod.Status.PUBLISHED
        self.period.save()

        # Tạo recommendation
        Recommendation.objects.create(
            student=self.student,
            topic=self.topic,
            final_score=83.5,
            m1_skill=80,
            m2_academic=85,
            m3_field=90,
        )

        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=self.topic,
            preference_rank=1,
            match_score=None,  # Để trống điểm trong Allocation
            status=Allocation.Status.OFFICIAL,
        )

        res = get_student_allocation_result(self.student, self.period.pk)
        self.assertTrue(res["is_published"])
        self.assertEqual(res["match_score"], 83.5)

    def test_manual_allocation_display_xep_bo_sung(self):
        """Khi SV được xếp bổ sung ở Pha 2 (preference_rank=None), giao diện hiện 'Xếp bổ sung'."""
        from allocate.models import Allocation
        from catalog.models import RegistrationPeriod

        self.period.status = RegistrationPeriod.Status.PUBLISHED
        self.period.save()

        Allocation.objects.create(
            period=self.period,
            student=self.student,
            topic=self.topic,
            preference_rank=None,  # Khoa chỉ định Pha 2
            match_score=78.0,
            status=Allocation.Status.OFFICIAL,
            source=Allocation.Source.MANUAL,
        )

        self.client.force_login(self.u_sv)

        # /ket-qua/
        r_kq = self.client.get("/ket-qua/")
        self.assertEqual(r_kq.status_code, 200)
        content_kq = r_kq.content.decode("utf-8")
        self.assertIn("Xếp bổ sung", content_kq)

        # /trang-chu/
        r_home = self.client.get("/trang-chu/")
        self.assertEqual(r_home.status_code, 200)
        content_home = r_home.content.decode("utf-8")
        self.assertIn("Xếp bổ sung", content_home)
