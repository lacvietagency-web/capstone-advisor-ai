"""Kiểm thử tự động cho module báo cáo thống kê Khoa (reports).

Bao gồm các kiểm thử cho:
1. get_registration_stats (tỷ lệ sinh viên đã/chưa đăng ký).
2. get_topic_nv1_distribution (phân bố NV1 theo đề tài, đề tài hot).
3. get_field_distribution (phân bố NV1 theo lĩnh vực).
4. get_lecturer_load (tải giảng viên theo chỉ tiêu).
5. compare_algorithms (so sánh ILP vs Greedy trên cùng đợt, không lưu CSDL).
6. View faculty_statistics (phân quyền và giao diện hiển thị).
"""

from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import User
from allocate.models import Allocation
from catalog.models import Field, Lecturer, Major, Preference, RegistrationPeriod, Student, Topic
from reports.services import (
    compare_algorithms,
    get_field_distribution,
    get_lecturer_load,
    get_registration_stats,
    get_topic_nv1_distribution,
)


@override_settings(RECOMMEND_SEMANTIC=False)
class ReportsServicesTestCase(TestCase):
    """Kiểm thử các hàm nghiệp vụ tính toán thống kê trong reports/services.py."""

    def setUp(self):
        """Khởi tạo dữ liệu mẫu tối giản để kiểm tra công thức chính xác."""
        self.major = Major.objects.create(name="Công nghệ thông tin")
        self.field_web = Field.objects.create(name="Web")
        self.field_ai = Field.objects.create(name="Trí tuệ nhân tạo")

        # Tạo 2 giảng viên
        self.u_lec1 = User.objects.create_user(
            username="gv1",
            first_name="Văn A",
            last_name="Nguyễn",
            role=User.Role.LECTURER,
        )
        self.lec1 = Lecturer.objects.create(user=self.u_lec1, department="CNTT", max_students=2)
        self.lec1.fields.add(self.field_web)

        self.u_lec2 = User.objects.create_user(
            username="gv2",
            first_name="Thị B",
            last_name="Trần",
            role=User.Role.LECTURER,
        )
        self.lec2 = Lecturer.objects.create(user=self.u_lec2, department="KTPM", max_students=3)
        self.lec2.fields.add(self.field_ai)

        # Tạo 3 đề tài
        self.topic1 = Topic.objects.create(
            lecturer=self.lec1,
            title="Website thương mại điện tử",
            description="Mô tả đề tài 1",
            capacity=1,
            status=Topic.Status.OPEN,
        )
        self.topic1.fields.add(self.field_web)

        self.topic2 = Topic.objects.create(
            lecturer=self.lec2,
            title="Nhận diện khuôn mặt bằng AI",
            description="Mô tả đề tài 2",
            capacity=2,
            status=Topic.Status.OPEN,
        )
        self.topic2.fields.add(self.field_ai)

        self.topic3 = Topic.objects.create(
            lecturer=self.lec2,
            title="Chatbot tư vấn tuyển sinh",
            description="Mô tả đề tài 3",
            capacity=2,
            status=Topic.Status.OPEN,
        )
        self.topic3.fields.add(self.field_ai, self.field_web)

        # Tạo 3 sinh viên
        self.students = []
        for i in range(1, 4):
            u = User.objects.create_user(username=f"sv{i}", role=User.Role.STUDENT)
            s = Student.objects.create(user=u, student_code=f"SV00{i}", major=self.major, gpa=3.2)
            self.students.append(s)

        # Tạo đợt đăng ký
        now = timezone.now()
        self.period = RegistrationPeriod.objects.create(
            name="Đợt 1 - 2026",
            start_at=now - timedelta(days=1),
            end_at=now + timedelta(days=7),
            status=RegistrationPeriod.Status.OPEN,
        )

        # SV1 chọn NV1: topic1, NV2: topic2
        Preference.objects.create(student=self.students[0], topic=self.topic1, period=self.period, rank=1)
        Preference.objects.create(student=self.students[0], topic=self.topic2, period=self.period, rank=2)

        # SV2 chọn NV1: topic1, NV2: topic3
        Preference.objects.create(student=self.students[1], topic=self.topic1, period=self.period, rank=1)
        Preference.objects.create(student=self.students[1], topic=self.topic3, period=self.period, rank=2)

        # SV3 chưa đăng ký nguyện vọng nào trong đợt này

    def test_get_registration_stats(self):
        """Kiểm tra tính toán số SV đã đăng ký / chưa đăng ký và tỷ lệ phần trăm."""
        stats = get_registration_stats(self.period)
        self.assertEqual(stats["total_students"], 3)
        self.assertEqual(stats["registered_students"], 2)
        self.assertEqual(stats["unregistered_students"], 1)
        self.assertAlmostEqual(stats["registered_rate"], 66.7, places=1)
        self.assertAlmostEqual(stats["unregistered_rate"], 33.3, places=1)

        # Kiểm tra khi period is None
        empty_stats = get_registration_stats(None)
        self.assertEqual(empty_stats["registered_students"], 0)
        self.assertEqual(empty_stats["unregistered_students"], 3)

    def test_get_topic_nv1_distribution(self):
        """Kiểm tra xếp hạng đề tài hot theo số lượng NV1."""
        topics = get_topic_nv1_distribution(self.period)
        self.assertEqual(len(topics), 1)  # Chỉ topic1 có NV1
        top1 = topics[0]
        self.assertEqual(top1["topic_id"], self.topic1.id)
        self.assertEqual(top1["nv1_count"], 2)
        self.assertEqual(top1["capacity"], 1)
        self.assertEqual(top1["competition_rate"], 2.0)  # 2 NV1 / 1 capacity
        self.assertEqual(top1["percentage"], 100.0)

        # Thêm NV1 cho topic2
        Preference.objects.create(student=self.students[2], topic=self.topic2, period=self.period, rank=1)
        topics = get_topic_nv1_distribution(self.period)
        self.assertEqual(len(topics), 2)
        self.assertEqual(topics[0]["topic_id"], self.topic1.id)
        self.assertEqual(topics[0]["nv1_count"], 2)
        self.assertEqual(topics[1]["topic_id"], self.topic2.id)
        self.assertEqual(topics[1]["nv1_count"], 1)
        self.assertAlmostEqual(topics[0]["percentage"], 66.7, places=1)
        self.assertAlmostEqual(topics[1]["percentage"], 33.3, places=1)

    def test_get_field_distribution(self):
        """Kiểm tra phân bố NV1 theo lĩnh vực."""
        fields = get_field_distribution(self.period)
        # topic1 thuộc lĩnh vực Web -> Web nhận 2 NV1
        web_field = next(f for f in fields if f["field_id"] == self.field_web.id)
        ai_field = next(f for f in fields if f["field_id"] == self.field_ai.id)

        self.assertEqual(web_field["count"], 2)
        self.assertEqual(web_field["percentage"], 100.0)
        self.assertEqual(ai_field["count"], 0)
        self.assertEqual(ai_field["percentage"], 0.0)

    def test_get_lecturer_load_with_allocations(self):
        """Kiểm tra tải giảng viên tính từ bảng Allocation trong cơ sở dữ liệu."""
        # Gán SV1 vào topic1 (thuộc lec1), SV2 vào topic2 (thuộc lec2)
        Allocation.objects.create(
            period=self.period,
            student=self.students[0],
            topic=self.topic1,
            preference_rank=1,
            status=Allocation.Status.DRAFT,
        )
        Allocation.objects.create(
            period=self.period,
            student=self.students[1],
            topic=self.topic2,
            preference_rank=2,
            status=Allocation.Status.DRAFT,
        )

        load = get_lecturer_load(self.period)
        self.assertEqual(len(load), 2)
        lec1_stat = next(l for l in load if l["lecturer_id"] == self.lec1.id)
        lec2_stat = next(l for l in load if l["lecturer_id"] == self.lec2.id)

        self.assertEqual(lec1_stat["assigned_count"], 1)
        self.assertEqual(lec1_stat["capacity"], 2)
        self.assertEqual(lec1_stat["load_rate"], 50.0)
        self.assertEqual(lec1_stat["status"], "Đang nhận")

        self.assertEqual(lec2_stat["assigned_count"], 1)
        self.assertEqual(lec2_stat["capacity"], 3)
        self.assertAlmostEqual(lec2_stat["load_rate"], 33.3, places=1)

    def test_get_lecturer_load_with_simulated_assignment(self):
        """Kiểm tra tải giảng viên khi truyền vào bản đồ phân công gán mô phỏng."""
        # assign: {s1_id: topic1_id, s2_id: topic1_id} -> lec1 nhận 2 SV (đầy chỉ tiêu)
        simulated_assign = {
            self.students[0].id: self.topic1.id,
            self.students[1].id: self.topic1.id,
        }
        load = get_lecturer_load(self.period, assign=simulated_assign)
        lec1_stat = next(l for l in load if l["lecturer_id"] == self.lec1.id)
        self.assertEqual(lec1_stat["assigned_count"], 2)
        self.assertEqual(lec1_stat["capacity"], 2)
        self.assertEqual(lec1_stat["load_rate"], 100.0)
        self.assertEqual(lec1_stat["status"], "Đầy chỉ tiêu")

    def test_compare_algorithms_simulation_no_db_side_effects(self):
        """Kiểm tra so sánh ILP và Greedy: chạy cả 2 bộ giải và KHÔNG lưu cơ sở dữ liệu."""
        initial_alloc_count = Allocation.objects.count()
        initial_status = self.period.status

        res = compare_algorithms(self.period)

        # Đảm bảo không có bản ghi Allocation nào được tạo hay sửa
        self.assertEqual(Allocation.objects.count(), initial_alloc_count)
        self.period.refresh_from_db()
        self.assertEqual(self.period.status, initial_status)

        # Kiểm tra cấu trúc kết quả
        self.assertIn("ilp", res)
        self.assertIn("greedy", res)
        self.assertIn("delta", res)

        ilp = res["ilp"]
        greedy = res["greedy"]

        # Các trường bắt buộc theo đặc tả
        for metric_set in (ilp, greedy):
            self.assertIn("nv1_pct", metric_set)
            self.assertIn("top3_pct", metric_set)
            self.assertIn("unassigned_count", metric_set)
            self.assertIn("unassigned_rate", metric_set)
            self.assertIn("assigned_pct", metric_set)
            self.assertIn("elapsed_time", metric_set)

        # Cả 2 sinh viên (SV1, SV2) phải được xếp do có đủ chỗ ở các nguyện vọng
        self.assertEqual(ilp["unassigned_count"], 0)
        self.assertEqual(ilp["assigned_pct"], 100.0)


@override_settings(RECOMMEND_SEMANTIC=False)
class FacultyStatisticsViewTestCase(TestCase):
    """Kiểm thử View /khoa/thong-ke/: phân quyền và hiển thị template."""

    def setUp(self):
        self.major = Major.objects.create(name="Hệ thống thông tin")
        self.field = Field.objects.create(name="Trí tuệ nhân tạo")

        # Tài khoản Khoa (Admin)
        self.admin_user = User.objects.create_user(
            username="admin_khoa",
            password="password123",
            role=User.Role.ADMIN,
        )

        # Tài khoản Giảng viên
        self.lecturer_user = User.objects.create_user(
            username="gv_test",
            password="password123",
            role=User.Role.LECTURER,
        )
        Lecturer.objects.create(user=self.lecturer_user, max_students=5)

        # Tài khoản Sinh viên
        self.student_user = User.objects.create_user(
            username="sv_test",
            password="password123",
            role=User.Role.STUDENT,
        )
        Student.objects.create(user=self.student_user, student_code="SV999", major=self.major, gpa=3.5)

        now = timezone.now()
        self.period = RegistrationPeriod.objects.create(
            name="Đợt 2 - 2026",
            start_at=now - timedelta(days=2),
            end_at=now + timedelta(days=5),
            status=RegistrationPeriod.Status.OPEN,
        )

    def test_permission_denied_for_non_faculty(self):
        """Khách vãng lai chuyển hướng đăng nhập; SV và GV bị 403 Forbidden."""
        # 1. Khách vãng lai
        res = self.client.get("/khoa/thong-ke/")
        self.assertEqual(res.status_code, 302)

        # 2. Sinh viên
        self.client.force_login(self.student_user)
        res = self.client.get("/khoa/thong-ke/")
        self.assertEqual(res.status_code, 403)

        # 3. Giảng viên
        self.client.force_login(self.lecturer_user)
        res = self.client.get("/khoa/thong-ke/")
        self.assertEqual(res.status_code, 403)

    def test_topic_count_not_capped_at_top10(self):
        """Ô "Đề tài" khớp Bảng điều khiển, không phải độ dài danh sách top 10 (phát hiện khi đóng vai trưởng khoa)."""
        lec = Lecturer.objects.get()
        Topic.objects.bulk_create(Topic(lecturer=lec, title=f"Đề tài {i}", description="x") for i in range(12))
        self.client.force_login(self.admin_user)
        res = self.client.get("/khoa/thong-ke/")
        self.assertEqual(res.context["n_topics"], 12)
        self.assertContains(res, '<div class="at-ledger-value">12</div>', html=True)

    def test_faculty_admin_can_access_dashboard(self):
        """Giáo vụ Khoa đăng nhập thành công vào trang thống kê."""
        self.client.force_login(self.admin_user)
        res = self.client.get("/khoa/thong-ke/")
        self.assertEqual(res.status_code, 200)

        # Kiểm tra các biến trong context
        self.assertIn("reg_stats", res.context)
        self.assertIn("topic_nv1_list", res.context)
        self.assertIn("field_list", res.context)
        self.assertIn("lecturer_load", res.context)
        self.assertIn("comparison", res.context)
        self.assertIn("chart_data", res.context)

        # Kiểm tra nội dung render
        content = res.content.decode("utf-8")
        self.assertIn("Thống kê &amp; Báo cáo Khoa", content)
        self.assertIn("cdn.jsdelivr.net/npm/chart.js", content)
        self.assertIn("stats-data", content)

    def test_period_id_query_parameter(self):
        """Kiểm tra tham số period_id khi chọn đợt khác."""
        now = timezone.now()
        other_period = RegistrationPeriod.objects.create(
            name="Đợt Cũ 2025",
            start_at=now - timedelta(days=100),
            end_at=now - timedelta(days=90),
            status=RegistrationPeriod.Status.CLOSED,
        )

        self.client.force_login(self.admin_user)
        res = self.client.get(f"/khoa/thong-ke/?period_id={other_period.pk}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["period"], other_period)
