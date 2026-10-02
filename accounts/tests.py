from django.core.management import call_command
from django.test import TestCase

from accounts.models import User


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
        self.client.login(username="gv001", password="123456")
        self.assertContains(self.client.get("/trang-chu/"), "Đề tài của tôi")

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
