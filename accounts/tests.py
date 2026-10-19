from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from catalog.models import Lecturer, Major, Preference, RegistrationPeriod, Student, Topic


class RoleAccessTests(TestCase):
    """Mỗi vai trò vào đúng trang của mình; SV/GV không vào được trang quản trị của Khoa."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=10, lecturers=3, topics=8, verbosity=0)
        User.objects.create_superuser("admin", "a@a.vn", "admin123")

    def test_student_home(self):
        self.client.login(username="sv001", password="123456")
        r = self.client.get("/trang-chu/")
        self.assertContains(r, "Nguyện vọng của bạn")
        self.assertEqual(self.client.get("/quan-tri/").status_code, 302)

    def test_lecturer_home(self):
        """Giảng viên đăng nhập vào /trang-chu/ thấy danh sách đề tài và các thẻ số liệu."""
        self.client.login(username="gv001", password="123456")
        resp = self.client.get("/trang-chu/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Đề tài của tôi")
        for label in ("Đề tài", "SV đăng ký", "Chờ duyệt", "Đã đồng ý"):  # nhãn thẻ số liệu đang hiển thị
            self.assertContains(resp, f'<div class="at-ledger-label">{label}</div>', html=True)
        self.assertIn("n_topics", resp.context)
        self.assertIn("n_students", resp.context)
        self.assertIn("n_pending", resp.context)
        self.assertIn("n_accepted", resp.context)

    def test_admin_home(self):
        self.client.login(username="admin", password="admin123")
        self.assertContains(self.client.get("/trang-chu/"), "Bảng điều khiển Khoa")
        self.assertEqual(self.client.get("/quan-tri/catalog/topic/").status_code, 200)

    def test_vietnamese_name_order(self):
        u = User(first_name="Thành", last_name="Trịnh Hoàng")
        self.assertEqual(u.get_full_name(), "Trịnh Hoàng Thành")


class PasswordChangeTests(TestCase):
    """Kiểm thử tính năng đổi mật khẩu (UC03):

    Quy trình và điều kiện:
    - Điều kiện tiền đề: người dùng đã xác thực (is_authenticated == True).
    - Công thức kiểm tra:
        1. check_password(old_password, user.password) == True.
        2. validate_password(new_password1, user) thoả mãn độ dài tối thiểu, không trùng thông tin,
           không nằm trong danh sách phổ biến.
        3. new_password1 == new_password2.
    - Cập nhật và lưu trữ:
        password_hash = make_password(new_password1)
        update_session_auth_hash(request, user)
    - Điều hướng thành công: redirect sang URL /doi-mat-khau/xong/ (HTTP 302).
    """

    @classmethod
    def setUpTestData(cls):
        """Khởi tạo người dùng thử nghiệm để thực hiện kiểm thử đổi mật khẩu."""
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="OldPassword123!",
            role=User.Role.STUDENT,
        )

    def test_anonymous_user_redirected_to_login(self):
        """Khách chưa đăng nhập truy cập /doi-mat-khau/ hoặc /doi-mat-khau/xong/ bị chuyển hướng về /dang-nhap/.

        Kiểm tra mã trạng thái HTTP 302 và URL đích có chứa tham số ?next=.
        """
        resp = self.client.get("/doi-mat-khau/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/dang-nhap/", resp.headers["Location"])

        resp_done = self.client.get("/doi-mat-khau/xong/")
        self.assertEqual(resp_done.status_code, 302)
        self.assertIn("/dang-nhap/", resp_done.headers["Location"])

    def test_authenticated_user_can_view_password_change_form(self):
        """Người dùng đã đăng nhập truy cập /doi-mat-khau/ nhận mã HTTP 200 và form đổi mật khẩu.

        Giao diện chứa đúng template registration/password_change_form.html và các trường nhập mật khẩu.
        """
        self.client.login(username="testuser", password="OldPassword123!")
        resp = self.client.get("/doi-mat-khau/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "registration/password_change_form.html")
        self.assertContains(resp, "Mật khẩu cũ")
        self.assertContains(resp, "Mật khẩu mới")
        self.assertContains(resp, "Xác nhận mật khẩu mới")

    def test_password_change_successful_flow(self):
        """Kiểm thử luồng đổi mật khẩu thành công:

        1. Gửi POST với old_password đúng và new_password1 == new_password2 hợp lệ.
        2. Nhận HTTP 302 chuyển hướng về /doi-mat-khau/xong/.
        3. Truy cập /doi-mat-khau/xong/ nhận HTTP 200 và giao diện thông báo thành công.
        4. Kiểm tra user.check_password: mật khẩu mới đúng, mật khẩu cũ không còn hợp lệ.
        5. Đăng xuất và đăng nhập lại bằng mật khẩu mới thành công.
        """
        self.client.login(username="testuser", password="OldPassword123!")
        new_pass = "NewStrongPass456#"
        resp = self.client.post(
            "/doi-mat-khau/",
            {
                "old_password": "OldPassword123!",
                "new_password1": new_pass,
                "new_password2": new_pass,
            },
        )
        self.assertRedirects(resp, "/doi-mat-khau/xong/")

        done_resp = self.client.get("/doi-mat-khau/xong/")
        self.assertEqual(done_resp.status_code, 200)
        self.assertTemplateUsed(done_resp, "registration/password_change_done.html")
        self.assertContains(done_resp, "Đổi mật khẩu thành công")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_pass))
        self.assertFalse(self.user.check_password("OldPassword123!"))

        self.client.logout()
        login_success = self.client.login(username="testuser", password=new_pass)
        self.assertTrue(login_success)

        self.client.logout()
        login_old_failed = self.client.login(username="testuser", password="OldPassword123!")
        self.assertFalse(login_old_failed)

    def test_password_change_wrong_old_password(self):
        """Nhập sai mật khẩu cũ:

        Điều kiện check_password(old_password) == False dẫn tới lỗi validation 'password_incorrect'.
        Mật khẩu trong CSDL không bị thay đổi.
        """
        self.client.login(username="testuser", password="OldPassword123!")
        resp = self.client.post(
            "/doi-mat-khau/",
            {
                "old_password": "SaiMatKhau123!",
                "new_password1": "NewStrongPass456#",
                "new_password2": "NewStrongPass456#",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("old_password", resp.context["form"].errors)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OldPassword123!"))

    def test_password_change_mismatched_new_passwords(self):
        """Hai lần nhập mật khẩu mới không khớp (new_password1 != new_password2):

        Form báo lỗi không khớp và mật khẩu trong CSDL được giữ nguyên.
        """
        self.client.login(username="testuser", password="OldPassword123!")
        resp = self.client.post(
            "/doi-mat-khau/",
            {
                "old_password": "OldPassword123!",
                "new_password1": "NewStrongPass456#",
                "new_password2": "KhacMatKhau456#",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("new_password2", resp.context["form"].errors)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OldPassword123!"))

    def test_password_change_weak_password_rejected(self):
        """Mật khẩu mới quá yếu (dưới 8 ký tự hoặc toàn chữ số):

        Bị chặn bởi các validator tiêu chuẩn của Django và form trả về lỗi.
        """
        self.client.login(username="testuser", password="OldPassword123!")
        resp = self.client.post(
            "/doi-mat-khau/",
            {
                "old_password": "OldPassword123!",
                "new_password1": "123",
                "new_password2": "123",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("new_password2", resp.context["form"].errors)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OldPassword123!"))

    def test_user_menu_contains_password_change_link(self):
        """Người dùng đăng nhập thấy liên kết 'Đổi mật khẩu' (/doi-mat-khau/) trong thanh menu điều hướng."""
        self.client.login(username="testuser", password="OldPassword123!")
        resp = self.client.get("/trang-chu/")
        self.assertContains(resp, 'href="/doi-mat-khau/"')
        self.assertContains(resp, "Đổi mật khẩu")

    def test_lecturer_user_can_also_change_password(self):
        """Giảng viên cũng đổi được mật khẩu theo đúng quy trình xác thực và băm mật khẩu mới."""
        lecturer_user = User.objects.create_user(
            username="testlec",
            email="lec@example.com",
            password="LecOldPass123!",
            role=User.Role.LECTURER,
        )
        self.client.login(username="testlec", password="LecOldPass123!")
        resp = self.client.post(
            "/doi-mat-khau/",
            {
                "old_password": "LecOldPass123!",
                "new_password1": "LecNewPass456#",
                "new_password2": "LecNewPass456#",
            },
        )
        self.assertRedirects(resp, "/doi-mat-khau/xong/")
        lecturer_user.refresh_from_db()
        self.assertTrue(lecturer_user.check_password("LecNewPass456#"))


class LecturerHomeDashboardTests(TestCase):
    """Kiểm thử màn hình trang chủ giảng viên (/trang-chu/, UC: Giảng viên theo dõi đề tài).

    Quy tắc và công thức toán học kiểm tra:
    1. Số đề tài do giảng viên phụ trách:
       N_topics = |{t in Topic | t.lecturer = lecturer}|
    2. Tổng sinh viên đăng ký vào các đề tài của giảng viên:
       N_students = |{s in Student | ton_tai p in Preference: p.student = s va p.topic.lecturer = lecturer}|
    3. Số nguyện vọng đang chờ duyệt:
       N_pending = |{p in Preference | p.topic.lecturer = lecturer va p.status = 'PENDING'}|
    4. Số nguyện vọng đã đồng ý:
       N_accepted = |{p in Preference | p.topic.lecturer = lecturer va p.status = 'ACCEPTED'}|
    5. Cột 'Chờ duyệt' cho từng đề tài:
       pending_count(t) = |{p in Preference | p.topic = t va p.status = 'PENDING'}|
    6. Điều hướng:
       Nút 'Duyệt ngay' dẫn tới /de-tai/<topic_id>/dang-ky/
    """

    @classmethod
    def setUpTestData(cls):
        """Khởi tạo dữ liệu thử nghiệm cho giảng viên, đề tài và các nguyện vọng đăng ký."""
        cls.major = Major.objects.create(name="Công nghệ thông tin")

        # Tạo tài khoản giảng viên chính
        cls.lec_user = User.objects.create_user(
            username="gv_main",
            email="gv_main@example.com",
            password="Password123!",
            role=User.Role.LECTURER,
            first_name="Hùng",
            last_name="Nguyễn Văn",
        )
        cls.lecturer = Lecturer.objects.create(user=cls.lec_user, department="CNTT", max_students=5)

        # Tạo 2 đề tài cho giảng viên chính
        cls.t1 = Topic.objects.create(
            lecturer=cls.lecturer,
            title="Đề tài AI 01",
            capacity=2,
            status=Topic.Status.OPEN,
        )
        cls.t2 = Topic.objects.create(
            lecturer=cls.lecturer,
            title="Đề tài Web 02",
            capacity=2,
            status=Topic.Status.OPEN,
        )

        # Tạo giảng viên khác và đề tài của họ để kiểm tra cách ly dữ liệu
        cls.other_user = User.objects.create_user(
            username="gv_other",
            email="gv_other@example.com",
            password="Password123!",
            role=User.Role.LECTURER,
        )
        cls.other_lec = Lecturer.objects.create(user=cls.other_user, department="KTPM", max_students=5)
        cls.t_other = Topic.objects.create(
            lecturer=cls.other_lec,
            title="Đề tài khác",
            capacity=1,
            status=Topic.Status.OPEN,
        )

        # Tạo đợt đăng ký
        cls.period = RegistrationPeriod.objects.create(
            name="Đợt 1 - 2026",
            start_at=timezone.now(),
            end_at=timezone.now(),
            status=RegistrationPeriod.Status.OPEN,
        )

        # Tạo 4 sinh viên
        cls.students = []
        for i in range(1, 5):
            u = User.objects.create_user(
                username=f"sv_test_{i}",
                password="Password123!",
                role=User.Role.STUDENT,
            )
            st = Student.objects.create(user=u, student_code=f"SV202600{i}", major=cls.major, gpa=3.2)
            cls.students.append(st)

        # Đăng ký nguyện vọng:
        # sv[0] -> t1 (PENDING)
        Preference.objects.create(
            student=cls.students[0], topic=cls.t1, period=cls.period, rank=1, status=Preference.Status.PENDING
        )
        # sv[1] -> t1 (PENDING)
        Preference.objects.create(
            student=cls.students[1], topic=cls.t1, period=cls.period, rank=1, status=Preference.Status.PENDING
        )
        # sv[1] -> t2 (ACCEPTED)  (sv[1] đăng ký 2 đề tài của cùng GV)
        Preference.objects.create(
            student=cls.students[1], topic=cls.t2, period=cls.period, rank=2, status=Preference.Status.ACCEPTED
        )
        # sv[2] -> t2 (ACCEPTED)
        Preference.objects.create(
            student=cls.students[2], topic=cls.t2, period=cls.period, rank=1, status=Preference.Status.ACCEPTED
        )
        # sv[3] -> t2 (REJECTED)
        Preference.objects.create(
            student=cls.students[3], topic=cls.t2, period=cls.period, rank=1, status=Preference.Status.REJECTED
        )
        # sv[3] -> t_other (PENDING - thuộc GV khác)
        Preference.objects.create(
            student=cls.students[3], topic=cls.t_other, period=cls.period, rank=2, status=Preference.Status.PENDING
        )

    def test_lecturer_dashboard_kpi_metrics(self):
        """Kiểm tra độ chính xác của 4 thẻ số liệu trên trang chủ giảng viên:

        N_topics = 2
        N_students = 4 (sv0, sv1, sv2, sv3)
        N_pending = 2 (t1: sv0 PENDING, sv1 PENDING)
        N_accepted = 2 (t2: sv1 ACCEPTED, sv2 ACCEPTED)
        """
        self.client.login(username="gv_main", password="Password123!")
        resp = self.client.get("/trang-chu/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "pages/home_lecturer.html")

        # Kiểm tra biến trong context
        self.assertEqual(resp.context["n_topics"], 2)
        self.assertEqual(resp.context["n_students"], 4)
        self.assertEqual(resp.context["n_pending"], 2)
        self.assertEqual(resp.context["n_accepted"], 2)

        # Kiểm tra hiển thị các thẻ số liệu
        for label in ("Đề tài", "SV đăng ký", "Chờ duyệt", "Đã đồng ý"):  # nhãn thẻ số liệu đang hiển thị
            self.assertContains(resp, f'<div class="at-ledger-label">{label}</div>', html=True)
        self.assertContains(resp, "Chờ duyệt")
        self.assertContains(resp, "Đã đồng ý")

    def test_topics_table_pending_column_and_review_links(self):
        """Trang chủ đếm SV chờ duyệt theo đề tài; trang Đề tài của tôi có nút 'SV đăng ký' hiện sẵn (không giấu trong menu)."""
        self.client.login(username="gv_main", password="Password123!")
        topics_page = self.client.get("/de-tai/")
        for t in (self.t1, self.t2):
            self.assertContains(
                topics_page,
                f'<a href="/de-tai/{t.pk}/dang-ky/" class="btn btn-secondary btn-sm">SV đăng ký</a>',
                count=2,  # một nút ở bảng (máy tính), một ở thẻ (điện thoại)
                html=True,
            )
        resp = self.client.get("/trang-chu/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Chờ duyệt")

        # Kiểm tra số lượng chờ duyệt của từng đề tài trong context
        topics = list(resp.context["topics"])
        topic_pending_map = {t.pk: t.pending_count for t in topics}
        self.assertEqual(topic_pending_map[self.t1.pk], 2)
        self.assertEqual(topic_pending_map[self.t2.pk], 0)

    def test_lecturer_with_no_topics_shows_zeros(self):
        """Giảng viên chưa đăng ký đề tài nào thì tất cả số liệu bằng 0."""
        new_lec_user = User.objects.create_user(
            username="gv_zero",
            password="Password123!",
            role=User.Role.LECTURER,
        )
        Lecturer.objects.create(user=new_lec_user, department="CNTT")

        self.client.login(username="gv_zero", password="Password123!")
        resp = self.client.get("/trang-chu/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["n_topics"], 0)
        self.assertEqual(resp.context["n_students"], 0)
        self.assertEqual(resp.context["n_pending"], 0)
        self.assertEqual(resp.context["n_accepted"], 0)
        self.assertContains(resp, "Chưa có đề tài")
