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
