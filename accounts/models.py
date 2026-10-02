from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Tài khoản đăng nhập. Mỗi người có đúng một vai trò; vai trò quyết định họ thấy trang nào."""

    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Sinh viên"
        LECTURER = "LECTURER", "Giảng viên"
        ADMIN = "ADMIN", "Khoa"

    role = models.CharField("Vai trò", max_length=10, choices=Role.choices, default=Role.STUDENT)

    def get_full_name(self):
        """Tên kiểu Việt: Họ đệm + Tên (Django mặc định ghép ngược kiểu Tây)."""
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_lecturer(self):
        return self.role == self.Role.LECTURER

    @property
    def is_faculty_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
