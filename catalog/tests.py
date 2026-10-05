from io import BytesIO
from pathlib import Path

import openpyxl
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from accounts.models import User
from catalog.admin import StudentAdmin
from catalog.importer import create_sample_excel, import_excel_data
from catalog.models import AuditLog, Field, Lecturer, Preference, RegistrationPeriod, Skill, Student, Topic
from recommend.models import Recommendation


def create_in_memory_workbook(sheets_data: dict[str, list[list]]) -> BytesIO:
    """Tạo workbook openpyxl trong bộ nhớ để phục vụ kiểm thử."""
    wb = openpyxl.Workbook()
    first = True
    for sheet_name, rows in sheets_data.items():
        if first:
            ws = wb.active
            ws.title = sheet_name
            first = False
        else:
            ws = wb.create_sheet(title=sheet_name)
        for row in rows:
            ws.append(row)
    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    return bio


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

    def eligible_topics(self, username, ok=True):
        from recommend.engine import Profile, eligible

        prof = Profile(Student.objects.get(user__username=username))
        return [t for t in Topic.objects.order_by("pk") if eligible(prof, t)[0] == ok]

    def student_with_choices(self, n=3):
        """SV đủ điều kiện ít nhất n đề tài (dữ liệu mẫu có lọc cứng nên không phải SV nào cũng đủ)."""
        for st in Student.objects.order_by("pk"):
            if len(self.eligible_topics(st.user.username)) >= n:
                return st.user.username
        self.fail(f"không có SV đủ điều kiện {n} đề tài")

    def test_ineligible_topic_is_rejected_with_reason(self):
        """Lọc cứng: SV không đăng ký được đề tài chưa đủ điều kiện (GPA / môn tiên quyết / kỹ năng bắt buộc)."""
        self.login("sv001")
        bad = self.eligible_topics("sv001", ok=False)
        self.assertTrue(bad, "dữ liệu mẫu phải có đề tài sv001 chưa đủ điều kiện")
        r = self.client.post("/nguyen-vong/", {"nv1": bad[0].pk})
        self.assertEqual(r.status_code, 200)  # form hiện lại với lỗi (đề tài không có trong danh sách được chọn)
        self.assertNotContains(r, f'value="{bad[0].pk}"')
        self.assertFalse(Preference.objects.filter(student__user__username="sv001", topic=bad[0]).exists())

    def test_resaving_preferences_keeps_lecturer_decision(self):
        """SV lưu lại nguyện vọng: đề tài giữ nguyên thì giữ kết quả GV đã duyệt; đề tài mới thì 'Chờ duyệt'."""
        sv = self.student_with_choices(3)
        self.login(sv)
        t1, t2, t3 = self.eligible_topics(sv)[:3]
        self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t2.pk})
        Preference.objects.filter(student__user__username=sv, topic=t1).update(status=Preference.Status.ACCEPTED)
        self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t3.pk})
        status = dict(Preference.objects.filter(student__user__username=sv).values_list("topic_id", "status"))
        self.assertEqual(status, {t1.pk: Preference.Status.ACCEPTED, t3.pk: Preference.Status.PENDING})

    def test_student_preferences_no_duplicates(self):
        sv = self.student_with_choices(2)
        self.login(sv)
        t1, t2 = self.eligible_topics(sv)[:2]
        r = self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t1.pk})
        self.assertContains(r, "không được trùng")
        self.client.post("/nguyen-vong/", {"nv1": t1.pk, "nv2": t2.pk})
        self.assertEqual(
            list(
                Preference.objects.filter(student__user__username=sv)
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

    def test_lecturer_registrations_view_and_accept(self):
        """[UC12] GV chủ đề tài xem danh sách đăng ký và duyệt Đồng ý nguyện vọng."""
        self.login("gv001")
        topic = Topic.objects.filter(lecturer__user__username="gv001").first()
        pref = Preference.objects.filter(topic=topic).first()
        self.assertIsNotNone(pref)
        self.assertEqual(pref.status, Preference.Status.PENDING)

        url = f"/de-tai/{topic.pk}/dang-ky/"
        r_get = self.client.get(url)
        self.assertEqual(r_get.status_code, 200)
        self.assertContains(r_get, "Đồng ý")
        self.assertContains(r_get, "Từ chối")

        r_post = self.client.post(url, {"preference_id": pref.pk, "action": "accept"})
        self.assertRedirects(r_post, url)
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.ACCEPTED)

        # Kiểm tra ghi AuditLog
        log = AuditLog.objects.filter(entity="Preference", entity_id=str(pref.pk)).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, "accept_registration")
        self.assertEqual(log.detail["status"], Preference.Status.ACCEPTED)

    def test_lecturer_registrations_reject(self):
        """[UC12] GV chủ đề tài từ chối nguyện vọng của sinh viên."""
        self.login("gv001")
        topic = Topic.objects.filter(lecturer__user__username="gv001").first()
        pref = Preference.objects.filter(topic=topic).first()
        self.assertIsNotNone(pref)

        url = f"/de-tai/{topic.pk}/dang-ky/"
        r_post = self.client.post(url, {"preference_id": pref.pk, "action": "reject"})
        self.assertRedirects(r_post, url)
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.REJECTED)

        # Kiểm tra ghi AuditLog
        log = AuditLog.objects.filter(entity="Preference", entity_id=str(pref.pk), action="reject_registration").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.detail["status"], Preference.Status.REJECTED)

    def test_only_topic_owner_can_manage_registrations(self):
        """[UC12] Chỉ GV chủ đề tài mới có quyền xem và duyệt đăng ký (GV khác bị 403)."""
        topic_gv1 = Topic.objects.filter(lecturer__user__username="gv001").first()
        pref = Preference.objects.filter(topic=topic_gv1).first()

        # gv002 đăng nhập và cố truy cập đề tài của gv001
        self.login("gv002")
        url = f"/de-tai/{topic_gv1.pk}/dang-ky/"
        r_get = self.client.get(url)
        self.assertEqual(r_get.status_code, 403)

        r_post = self.client.post(url, {"preference_id": pref.pk, "action": "accept"})
        self.assertEqual(r_post.status_code, 403)

        # Sinh viên đăng nhập cũng bị 403
        self.client.logout()
        self.login("sv001")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.post(url, {"preference_id": pref.pk, "action": "accept"}).status_code, 403)

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

    def pick(self, ok=True):
        """(username, đề tài) mà SV đó đủ / chưa đủ điều kiện — dữ liệu mẫu có lọc cứng."""
        from recommend.engine import Profile, eligible

        for st in Student.objects.order_by("pk"):
            prof = Profile(st)
            for t in Topic.objects.filter(status=Topic.Status.OPEN).order_by("pk"):
                if eligible(prof, t)[0] == ok:
                    return st.user.username, t
        self.skipTest("dữ liệu mẫu không có cặp phù hợp")

    def test_ineligible_topic_hides_register_and_shows_reason(self):
        """Đề tài SV chưa đủ điều kiện: không có nút đăng ký, hiện lý do."""
        user, topic = self.pick(ok=False)
        self.login(user)
        response = self.client.get(f"/danh-sach-de-tai/{topic.id}/")
        self.assertContains(response, "Bạn chưa đủ điều kiện đăng ký đề tài này")
        self.assertNotContains(response, f"?topic={topic.id}")

    def test_student_sees_score_and_register_button(self):
        """Sinh viên đăng nhập thấy điểm phù hợp (nếu có) và nút đăng ký nguyện vọng."""
        user, topic = self.pick()
        self.login(user)
        student = Student.objects.get(user__username=user)
        Recommendation.objects.filter(student=student, topic=topic).delete()
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
        user, topic = self.pick()
        self.login(user)
        student = Student.objects.get(user__username=user)
        Recommendation.objects.filter(student=student).delete()

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


@override_settings(RECOMMEND_SEMANTIC=False)
class ExcelImportTests(TestCase):
    """Kiểm thử toàn diện chức năng nhập dữ liệu từ Excel cho Khoa (UC15).

    Đặc tả kiểm tra:
        - Sheet SinhVien (mã, họ, tên, GPA, email)
        - Sheet GiangVien, DeTai, KyNang
        - Sử dụng thư viện openpyxl
        - Báo lỗi chi tiết theo dòng
        - Không lưu dữ liệu khi có lỗi (transaction atomic rollback)
        - Lệnh quản trị import_excel <file.xlsx>
        - Action và giao diện trong trang quản trị
        - File mẫu catalog/mau_nhap_lieu.xlsx tạo bằng code
    """

    def setUp(self):
        import tempfile

        # ghi ra thư mục tạm: kiểm thử không được sửa file mẫu catalog/mau_nhap_lieu.xlsx trong repo
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.sample_path = Path(self._tmp.name) / "mau_nhap_lieu.xlsx"

    def test_create_sample_excel_file(self):
        """Kiểm tra tệp catalog/mau_nhap_lieu.xlsx được tạo đầy đủ 4 sheet chuẩn."""
        create_sample_excel(self.sample_path)
        self.assertTrue(self.sample_path.exists())
        wb = openpyxl.load_workbook(self.sample_path)
        self.assertIn("SinhVien", wb.sheetnames)
        self.assertIn("GiangVien", wb.sheetnames)
        self.assertIn("DeTai", wb.sheetnames)
        self.assertIn("KyNang", wb.sheetnames)

        # Kiểm tra tiêu đề sheet SinhVien
        sv_headers = [cell for cell in next(wb["SinhVien"].iter_rows(values_only=True)) if cell]
        self.assertIn("Mã sinh viên", sv_headers)
        self.assertIn("GPA", sv_headers)
        self.assertIn("Email", sv_headers)

    def test_import_sample_excel_success(self):
        """Kiểm tra nhập thành công dữ liệu từ tệp mẫu."""
        create_sample_excel(self.sample_path)
        success, errors, stats = import_excel_data(self.sample_path)
        self.assertTrue(success)
        self.assertEqual(errors, [])
        self.assertEqual(stats["students"], 3)
        self.assertEqual(stats["lecturers"], 3)
        self.assertEqual(stats["topics"], 3)
        self.assertEqual(stats["skills"], 6)

        # Kiểm tra tính toàn vẹn dữ liệu sinh viên trong CSDL
        sv = Student.objects.get(student_code="SV001")
        self.assertEqual(sv.user.first_name, "An")
        self.assertEqual(sv.user.last_name, "Nguyễn Văn")
        self.assertEqual(float(sv.gpa), 3.50)
        self.assertEqual(sv.user.email, "an.nv@eaut.edu.vn")
        self.assertEqual(sv.user.role, User.Role.STUDENT)

        # Kiểm tra giảng viên và đề tài
        gv = Lecturer.objects.get(user__username="GV001")
        self.assertEqual(gv.department, "Khoa CNTT")
        self.assertEqual(gv.max_students, 5)

        topic = Topic.objects.get(title__icontains="Hệ thống gợi ý")
        self.assertEqual(topic.lecturer, gv)
        self.assertEqual(topic.difficulty, Topic.Difficulty.MEDIUM)
        self.assertTrue(topic.fields.filter(name="Trí tuệ nhân tạo").exists())

    def test_import_command_success(self):
        """Kiểm tra lệnh quản trị import_excel <file.xlsx> thực thi thành công."""
        create_sample_excel(self.sample_path)
        from io import StringIO

        out = StringIO()
        call_command("import_excel", str(self.sample_path), stdout=out)
        self.assertIn("Đã nhập thành công", out.getvalue())
        self.assertTrue(Student.objects.filter(student_code="SV001").exists())

    def test_import_command_file_not_found(self):
        """Kiểm tra lệnh import_excel báo lỗi khi file không tồn tại."""
        with self.assertRaises(CommandError) as ctx:
            call_command("import_excel", "non_existent_file_xyz.xlsx")
        self.assertIn("không tồn tại", str(ctx.exception))

    def test_invalid_gpa_row_error_and_transaction_rollback(self):
        """Kiểm tra báo lỗi theo dòng khi GPA > 4.0 và hoàn tác giao dịch không lưu gì."""
        data = {
            "SinhVien": [
                ["Mã sinh viên", "Họ đệm", "Tên", "GPA", "Email"],
                ["SV101", "Nguyễn", "Hoàng", 3.2, "hoang@eaut.edu.vn"],
                ["SV102", "Trần", "Tuấn", 4.5, "tuan@eaut.edu.vn"],  # Dòng 3 lỗi GPA > 4.0
                ["SV103", "Lê", "Minh", 2.9, "minh@eaut.edu.vn"],
            ]
        }
        bio = create_in_memory_workbook(data)
        success, errors, stats = import_excel_data(bio)

        self.assertFalse(success)
        self.assertTrue(any("dòng 3" in e.lower() and "gpa" in e.lower() for e in errors))
        # Khẳng định không có sinh viên nào được lưu vào CSDL (Atomic rollback)
        self.assertEqual(Student.objects.count(), 0)
        self.assertEqual(User.objects.filter(username__in=["SV101", "SV102", "SV103"]).count(), 0)

    def test_invalid_email_and_missing_fields_row_errors(self):
        """Kiểm tra báo lỗi theo dòng khi email sai định dạng hoặc thiếu trường bắt buộc."""
        data = {
            "SinhVien": [
                ["Mã sinh viên", "Họ đệm", "Tên", "GPA", "Email"],
                ["", "Nguyễn", "Thiếu Mã", 3.0, "m@eaut.edu.vn"],  # Dòng 2 thiếu mã
                ["SV202", "Trần", "", 3.5, "t@eaut.edu.vn"],  # Dòng 3 thiếu tên
                ["SV203", "Lê", "An", 3.5, "invalid-email"],  # Dòng 4 sai email
            ]
        }
        bio = create_in_memory_workbook(data)
        success, errors, _ = import_excel_data(bio)

        self.assertFalse(success)
        self.assertTrue(any("dòng 2" in e.lower() and "mã" in e.lower() for e in errors))
        self.assertTrue(any("dòng 3" in e.lower() and "tên" in e.lower() for e in errors))
        self.assertTrue(any("dòng 4" in e.lower() and "email" in e.lower() for e in errors))
        self.assertEqual(Student.objects.count(), 0)

    def test_duplicate_student_code_in_file_rollback(self):
        """Kiểm tra trùng mã sinh viên ngay trong tệp Excel."""
        data = {
            "SinhVien": [
                ["Mã sinh viên", "Họ đệm", "Tên", "GPA", "Email"],
                ["SV301", "Nguyễn", "Văn A", 3.0, "a@eaut.edu.vn"],
                ["SV301", "Nguyễn", "Văn B", 3.2, "b@eaut.edu.vn"],  # Dòng 3 trùng mã
            ]
        }
        bio = create_in_memory_workbook(data)
        success, errors, _ = import_excel_data(bio)

        self.assertFalse(success)
        self.assertTrue(any("dòng 3" in e.lower() and "trùng lặp" in e.lower() for e in errors))
        self.assertEqual(Student.objects.count(), 0)

    def test_detai_missing_lecturer_rollback(self):
        """Kiểm tra đề tài trỏ tới giảng viên không tồn tại thì báo lỗi và rollback."""
        data = {
            "DeTai": [
                ["Tên đề tài", "Mã giảng viên", "Mô tả", "Lĩnh vực"],
                ["Đề tài không có GV", "GV_KHONG_TON_TAI", "Mô tả", "Web"],
            ]
        }
        bio = create_in_memory_workbook(data)
        success, errors, _ = import_excel_data(bio)

        self.assertFalse(success)
        self.assertTrue(any("dòng 2" in e.lower() and "giảng viên" in e.lower() for e in errors))
        self.assertEqual(Topic.objects.count(), 0)

    def test_kynang_duplicate_in_file(self):
        """Kiểm tra trùng kỹ năng trong cùng sheet KyNang."""
        data = {
            "KyNang": [
                ["Tên kỹ năng", "Lĩnh vực"],
                ["Django", "Web"],
                ["Django", "Web"],  # Trùng lặp
            ]
        }
        bio = create_in_memory_workbook(data)
        success, errors, _ = import_excel_data(bio)

        self.assertFalse(success)
        self.assertTrue(any("dòng 3" in e.lower() and "trùng lặp" in e.lower() for e in errors))
        self.assertEqual(Skill.objects.count(), 0)

    def test_invalid_file_format(self):
        """Kiểm tra xử lý khi tệp tải lên không phải định dạng Excel hợp lệ."""
        fake_file = BytesIO(b"Day khong phai la file excel")
        success, errors, _ = import_excel_data(fake_file)
        self.assertFalse(success)
        self.assertTrue(any("không đúng định dạng" in e.lower() for e in errors))

    def test_admin_import_views_and_action(self):
        """Kiểm tra action và giao diện import trong Django Admin."""
        User.objects.create_superuser("admin_test", "admin@eaut.edu.vn", "123456")
        self.client.login(username="admin_test", password="123456")

        from django.urls import reverse

        # 1. GET giao diện import
        url_import = reverse("admin:catalog_student_import_excel")
        resp = self.client.get(url_import)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Nhập dữ liệu từ Excel")

        # 2. GET tải tệp mẫu
        url_sample = reverse("admin:catalog_student_sample_excel")
        resp_sample = self.client.get(url_sample)
        self.assertEqual(resp_sample.status_code, 200)
        self.assertEqual(
            resp_sample["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # 3. POST tệp hợp lệ qua giao diện admin
        create_sample_excel(self.sample_path)
        with open(self.sample_path, "rb") as f:
            upload_file = SimpleUploadedFile(
                "mau_nhap_lieu.xlsx",
                f.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            resp_post = self.client.post(url_import, {"excel_file": upload_file}, follow=True)
            self.assertEqual(resp_post.status_code, 200)
            self.assertContains(resp_post, "Nhập dữ liệu thành công")
            self.assertTrue(Student.objects.filter(student_code="SV001").exists())
            self.assertTrue(AuditLog.objects.filter(action="import_excel").exists())

    def test_admin_action_direct_call(self):
        """Kiểm tra gọi trực tiếp action import_excel trên StudentAdmin."""
        admin_user = User.objects.create_superuser("admin_test2", "admin2@eaut.edu.vn", "123456")
        self.client.login(username="admin_test2", password="123456")
        from django.contrib.admin.sites import site
        from django.test import RequestFactory

        rf = RequestFactory()
        create_sample_excel(self.sample_path)
        with open(self.sample_path, "rb") as f:
            from django.urls import reverse

            upload_file = SimpleUploadedFile("mau.xlsx", f.read())
            req = rf.post(
                reverse("admin:catalog_student_changelist"),
                {"action": "import_excel", "apply": "1"},
            )
            req.user = admin_user
            req.FILES["excel_file"] = upload_file
            # Giả lập messages framework trên request
            from django.contrib.messages.storage.fallback import FallbackStorage

            req.session = "session"
            messages = FallbackStorage(req)
            req._messages = messages

            st_admin = StudentAdmin(Student, site)
            res = st_admin.import_excel(req, Student.objects.none())
            self.assertEqual(res.status_code, 302)
            self.assertTrue(Student.objects.filter(student_code="SV001").exists())
