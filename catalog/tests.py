from django.core.management import call_command
from django.test import TestCase, override_settings

from accounts.models import User
from catalog.models import Field, Lecturer, Preference, RegistrationPeriod, Skill, Student, Topic
from recommend.models import Recommendation


@override_settings(RECOMMEND_SEMANTIC=False)
class BusinessFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=6, verbosity=0)
        User.objects.create_user(
            username="admin001",
            password="123456",
            role=User.Role.ADMIN,
            first_name="Ban",
            last_name="CNK",
        )

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

    def test_lecturer_profile_get_open_period(self):
        self.login("gv001")
        r = self.client.get("/ho-so-giang-vien/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Hồ sơ Giảng viên")
        self.assertFalse(r.context["is_locked"])

    def test_lecturer_updates_profile_when_open(self):
        self.login("gv001")
        lec = Lecturer.objects.get(user__username="gv001")
        f1, f2 = Field.objects.all()[:2]
        r = self.client.post(
            "/ho-so-giang-vien/",
            {
                "department": "Bộ môn Công nghệ phần mềm",
                "fields": [f1.pk, f2.pk],
                "max_students": 10,
            },
        )
        self.assertEqual(r.status_code, 302)
        lec.refresh_from_db()
        self.assertEqual(lec.department, "Bộ môn Công nghệ phần mềm")
        self.assertEqual(lec.max_students, 10)
        self.assertEqual(set(lec.fields.values_list("pk", flat=True)), {f1.pk, f2.pk})

    def test_lecturer_cannot_update_quota_when_period_closed(self):
        period = RegistrationPeriod.objects.first()
        period.status = RegistrationPeriod.Status.CLOSED
        period.save()

        self.login("gv001")
        lec = Lecturer.objects.get(user__username="gv001")
        old_quota = lec.max_students
        new_quota = old_quota + 5

        r_get = self.client.get("/ho-so-giang-vien/")
        self.assertEqual(r_get.status_code, 200)
        self.assertTrue(r_get.context["is_locked"])
        self.assertContains(r_get, "khoá")

        f = Field.objects.first()
        r_post = self.client.post(
            "/ho-so-giang-vien/",
            {
                "department": "Bộ môn Trí tuệ nhân tạo",
                "fields": [f.pk],
                "max_students": new_quota,
            },
        )
        self.assertEqual(r_post.status_code, 200)
        self.assertContains(r_post, "chỉ Khoa mới có quyền")
        lec.refresh_from_db()
        self.assertEqual(lec.max_students, old_quota)

    def test_lecturer_can_update_dept_and_fields_when_period_closed(self):
        period = RegistrationPeriod.objects.first()
        period.status = RegistrationPeriod.Status.CLOSED
        period.save()

        self.login("gv001")
        lec = Lecturer.objects.get(user__username="gv001")
        old_quota = lec.max_students
        f = Field.objects.first()

        r_post = self.client.post(
            "/ho-so-giang-vien/",
            {
                "department": "Bộ môn Hệ thống thông tin",
                "fields": [f.pk],
                "max_students": old_quota,
            },
        )
        self.assertEqual(r_post.status_code, 302)
        lec.refresh_from_db()
        self.assertEqual(lec.department, "Bộ môn Hệ thống thông tin")
        self.assertEqual(lec.max_students, old_quota)
        self.assertEqual(list(lec.fields.values_list("pk", flat=True)), [f.pk])

    def test_faculty_admin_can_update_quota_when_period_closed(self):
        period = RegistrationPeriod.objects.first()
        period.status = RegistrationPeriod.Status.CLOSED
        period.save()

        lec = Lecturer.objects.get(user__username="gv001")
        f = Field.objects.first()

        self.login("admin001")
        r = self.client.post(
            f"/ho-so-giang-vien/{lec.pk}/",
            {
                "department": "Bộ môn Khoa học dữ liệu",
                "fields": [f.pk],
                "max_students": 15,
            },
        )
        self.assertEqual(r.status_code, 302)
        lec.refresh_from_db()
        self.assertEqual(lec.department, "Bộ môn Khoa học dữ liệu")
        self.assertEqual(lec.max_students, 15)

    def test_student_cannot_access_lecturer_profile(self):
        self.login("sv001")
        self.assertEqual(self.client.get("/ho-so-giang-vien/").status_code, 403)
        self.assertEqual(self.client.post("/ho-so-giang-vien/", {}).status_code, 403)

    def test_unauthenticated_user_redirected(self):
        r = self.client.get("/ho-so-giang-vien/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/dang-nhap/", r.url)

    def test_lecturer_cannot_access_another_lecturer_profile(self):
        self.login("gv001")
        gv2 = Lecturer.objects.get(user__username="gv002")
        r = self.client.get(f"/ho-so-giang-vien/{gv2.pk}/")
        self.assertEqual(r.status_code, 403)


@override_settings(RECOMMEND_SEMANTIC=False)
class TopicFilterTests(TestCase):
    """Kiểm thử tính năng lọc đề tài: theo lĩnh vực, giảng viên, độ khó, tìm kiếm tên và phân trang."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=6, verbosity=0)

    def test_filter_by_field(self):
        """Lọc theo lĩnh vực trả về đúng các đề tài thuộc lĩnh vực đó."""
        field = Field.objects.first()
        expected_ids = set(Topic.objects.filter(status=Topic.Status.OPEN, fields=field).values_list("id", flat=True))
        response = self.client.get(f"/danh-sach-de-tai/?field={field.id}")
        self.assertEqual(response.status_code, 200)
        actual_ids = {t.id for t in response.context["page_obj"]}
        self.assertEqual(actual_ids, expected_ids)

    def test_filter_by_lecturer(self):
        """Lọc theo giảng viên trả về đúng các đề tài của giảng viên đó."""
        lecturer = Lecturer.objects.first()
        expected_ids = set(
            Topic.objects.filter(status=Topic.Status.OPEN, lecturer=lecturer).values_list("id", flat=True)
        )
        response = self.client.get(f"/danh-sach-de-tai/?lecturer={lecturer.id}")
        self.assertEqual(response.status_code, 200)
        actual_ids = {t.id for t in response.context["page_obj"]}
        self.assertEqual(actual_ids, expected_ids)

    def test_filter_by_difficulty(self):
        """Lọc theo độ khó trả về đúng đề tài có độ khó tương ứng."""
        difficulty = Topic.Difficulty.MEDIUM
        expected_ids = set(
            Topic.objects.filter(status=Topic.Status.OPEN, difficulty=difficulty).values_list("id", flat=True)
        )
        response = self.client.get(f"/danh-sach-de-tai/?difficulty={difficulty}")
        self.assertEqual(response.status_code, 200)
        actual_ids = {t.id for t in response.context["page_obj"]}
        self.assertEqual(actual_ids, expected_ids)

    def test_search_by_title(self):
        """Tìm kiếm theo tên đề tài (không phân biệt hoa thường)."""
        first_topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        keyword = first_topic.title.split()[0]
        response = self.client.get(f"/danh-sach-de-tai/?q={keyword}")
        self.assertEqual(response.status_code, 200)
        for t in response.context["page_obj"]:
            self.assertIn(keyword.lower(), t.title.lower())

    def test_combined_filters(self):
        """Kết hợp nhiều điều kiện lọc đồng thời."""
        target = Topic.objects.filter(status=Topic.Status.OPEN).first()
        field = target.fields.first()
        response = self.client.get(
            f"/danh-sach-de-tai/?field={field.id}&lecturer={target.lecturer.id}&difficulty={target.difficulty}&q={target.title}"
        )
        self.assertEqual(response.status_code, 200)
        actual_ids = {t.id for t in response.context["page_obj"]}
        self.assertIn(target.id, actual_ids)

    def test_pagination(self):
        """Phân trang danh sách đề tài và kiểm tra số lượng trên trang."""
        response = self.client.get("/danh-sach-de-tai/?per_page=2&page=1")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj), 2)
        self.assertTrue(page_obj.has_next())

        response_page2 = self.client.get("/danh-sach-de-tai/?per_page=2&page=2")
        self.assertEqual(response_page2.status_code, 200)
        page2_obj = response_page2.context["page_obj"]
        self.assertEqual(len(page2_obj), 2)
        # Trang 1 và trang 2 không trùng đề tài
        self.assertTrue(set(t.id for t in page_obj).isdisjoint(set(t.id for t in page2_obj)))


@override_settings(RECOMMEND_SEMANTIC=False)
class TopicPermissionAndDetailTests(TestCase):
    """Kiểm thử quyền truy cập và nội dung hiển thị chi tiết đề tài."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=6, verbosity=0)

    def login(self, username):
        self.client.login(username=username, password="123456")

    def test_anonymous_can_view_topic_list_and_detail(self):
        """Khách chưa đăng nhập xem được danh sách và chi tiết đề tài nhưng không thấy nút đăng ký NV."""
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        r_list = self.client.get("/danh-sach-de-tai/")
        self.assertEqual(r_list.status_code, 200)
        self.assertContains(r_list, topic.title)

        r_detail = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(r_detail.status_code, 200)
        self.assertContains(r_detail, topic.title)
        self.assertContains(r_detail, topic.description)
        # Khách không có nút đăng ký nguyện vọng và không có điểm phù hợp cá nhân
        self.assertNotContains(r_detail, "Đăng ký nguyện vọng")
        self.assertNotContains(r_detail, "Mức độ phù hợp với hồ sơ của bạn")

    def test_student_sees_score_and_register_button(self):
        """Sinh viên đăng nhập thấy điểm phù hợp (nếu có) và nút đăng ký nguyện vọng."""
        self.login("sv001")
        student = Student.objects.get(user__username="sv001")
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        rec = Recommendation.objects.create(
            student=student,
            topic=topic,
            m1_skill=80.0,
            m2_academic=75.0,
            m3_field=90.0,
            final_score=82.0,
            reason="Kỹ năng phù hợp tốt với yêu cầu đề tài.",
        )

        response = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Đăng ký nguyện vọng")
        self.assertContains(response, "Mức độ phù hợp với hồ sơ của bạn")
        self.assertContains(response, f"{rec.final_score:.0f}")
        self.assertContains(response, "Kỹ năng phù hợp tốt với yêu cầu đề tài.")

    def test_student_views_topic_without_recommendation(self):
        """Sinh viên xem đề tài chưa có gợi ý vẫn thấy nút đăng ký nhưng thấy thông báo chưa có điểm."""
        self.login("sv001")
        student = Student.objects.get(user__username="sv001")
        Recommendation.objects.filter(student=student).delete()
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()

        response = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Đăng ký nguyện vọng")
        self.assertContains(response, "Chưa có điểm đánh giá phù hợp")

    def test_student_sees_topic_detail_elements(self):
        """Trang chi tiết đề tài hiển thị đầy đủ: mô tả, kỹ năng yêu cầu, môn tiên quyết, sức chứa, số NV1."""
        self.login("sv001")
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()

        response = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, topic.description)
        self.assertContains(response, "Kỹ năng yêu cầu")
        self.assertContains(response, "Môn học tiên quyết")
        self.assertContains(response, "Sức chứa")
        self.assertContains(response, f"{topic.capacity} sinh viên")
        self.assertContains(response, "Số người đã đăng ký NV1")

    def test_lecturer_views_detail_without_register_button(self):
        """Giảng viên xem chi tiết đề tài nhưng không thấy nút đăng ký nguyện vọng của sinh viên."""
        self.login("gv001")
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()

        response = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Đăng ký nguyện vọng")
        self.assertNotContains(response, "Mức độ phù hợp với hồ sơ của bạn")

    def test_draft_topic_permission(self):
        """Đề tài nháp DRAFT chỉ tác giả được xem; sinh viên và khách bị 404; không xuất hiện ở danh sách."""
        gv1 = Lecturer.objects.get(user__username="gv001")
        draft_topic = Topic.objects.create(
            lecturer=gv1,
            title="Đề tài nháp thử nghiệm bảo mật",
            description="Mô tả đề tài nháp chưa công bố",
            status=Topic.Status.DRAFT,
            difficulty=Topic.Difficulty.HARD,
            capacity=2,
        )

        # 1. Không xuất hiện trong danh sách đề tài mở
        r_list = self.client.get("/danh-sach-de-tai/")
        self.assertNotContains(r_list, draft_topic.title)

        # 2. Khách vãng lai truy cập nhận 404
        r_anon = self.client.get(f"/danh-sach-de-tai/{draft_topic.id}/")
        self.assertEqual(r_anon.status_code, 404)

        # 3. Sinh viên truy cập nhận 404
        self.login("sv001")
        r_student = self.client.get(f"/danh-sach-de-tai/{draft_topic.id}/")
        self.assertEqual(r_student.status_code, 404)
        self.client.logout()

        # 4. Giảng viên khác truy cập nhận 404
        self.login("gv002")
        r_other_lec = self.client.get(f"/danh-sach-de-tai/{draft_topic.id}/")
        self.assertEqual(r_other_lec.status_code, 404)
        self.client.logout()

        # 5. Chính giảng viên tạo đề tài xem được (200)
        self.login("gv001")
        r_owner = self.client.get(f"/danh-sach-de-tai/{draft_topic.id}/")
        self.assertEqual(r_owner.status_code, 200)
        self.assertContains(r_owner, draft_topic.title)

    def test_nv1_count_accuracy(self):
        """Số người đã đăng ký NV1 được tính chính xác."""
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()

        # Đếm ban đầu
        initial_nv1 = Preference.objects.filter(topic=topic, rank=1).count()
        r_detail = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertEqual(r_detail.context["nv1_count"], initial_nv1)

    def test_register_button_redirects_and_presets_topic(self):
        """Bấm đăng ký nguyện vọng dẫn tới trang nguyện vọng và điền trước đề tài vào ô trống."""
        self.login("sv001")
        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        # Xóa nguyện vọng cũ của sv001 để test điền trước
        Preference.objects.filter(student__user__username="sv001").delete()

        response = self.client.get(f"/nguyen-vong/?topic={topic.id}")
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.initial.get("nv1"), topic)


@override_settings(RECOMMEND_SEMANTIC=False)
class CatalogServiceTests(TestCase):
    """Kiểm thử trực tiếp tầng dịch vụ catalog/services.py."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=6, verbosity=0)

    def test_get_visible_topics_only_open(self):
        """Dịch vụ get_visible_topics chỉ trả về đề tài có trạng thái OPEN."""
        from catalog.services import get_visible_topics

        lec = Lecturer.objects.first()
        closed_topic = Topic.objects.create(
            lecturer=lec,
            title="Đề tài đã đóng",
            description="Mô tả",
            status=Topic.Status.CLOSED,
            capacity=1,
        )
        draft_topic = Topic.objects.create(
            lecturer=lec,
            title="Đề tài nháp",
            description="Mô tả",
            status=Topic.Status.DRAFT,
            capacity=1,
        )
        visible = get_visible_topics()
        self.assertNotIn(closed_topic, visible)
        self.assertNotIn(draft_topic, visible)
        self.assertTrue(all(t.status == Topic.Status.OPEN for t in visible))

    def test_filter_topics_service_no_matches(self):
        """Bộ lọc trả về rỗng khi không có đề tài nào thỏa mãn tiêu chí."""
        from catalog.services import filter_topics, get_visible_topics

        visible = get_visible_topics()
        result = filter_topics(visible, query="Chuỗi tìm kiếm không bao giờ tồn tại XYZ123")
        self.assertEqual(result.count(), 0)

    def test_paginate_topics_service_edge_cases(self):
        """Phân trang xử lý trang không phải số và trang vượt quá phạm vi."""
        from catalog.services import get_visible_topics, paginate_topics

        visible = get_visible_topics()
        # Không phải số -> về trang 1
        page1 = paginate_topics(visible, page_number="not-a-number", per_page=2)
        self.assertEqual(page1.number, 1)

        # Vượt quá số trang -> về trang cuối
        last_page = paginate_topics(visible, page_number=9999, per_page=2)
        self.assertEqual(last_page.number, page1.paginator.num_pages)

    def test_get_topic_nv1_count_service(self):
        """Hàm get_topic_nv1_count đếm chính xác số lượng NV1."""
        from catalog.services import get_topic_nv1_count

        topic = Topic.objects.filter(status=Topic.Status.OPEN).first()
        period = RegistrationPeriod.objects.first()
        st1, st2 = Student.objects.all()[:2]

        Preference.objects.filter(topic=topic).delete()
        Preference.objects.filter(student__in=[st1, st2], period=period).delete()
        self.assertEqual(get_topic_nv1_count(topic), 0)

        Preference.objects.create(student=st1, topic=topic, period=period, rank=1)
        self.assertEqual(get_topic_nv1_count(topic), 1)

        # Đăng ký NV2 không được tính vào NV1
        Preference.objects.create(student=st2, topic=topic, period=period, rank=2)
        self.assertEqual(get_topic_nv1_count(topic), 1)
