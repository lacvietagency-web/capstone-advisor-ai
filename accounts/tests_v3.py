"""Kiểm thử phần lõi cho giao diện V3 (ATLAS): gợi ý tự tính, hành trình SV, nguyện vọng chỉ xem, bảng phân công."""

from django.core.management import call_command
from django.test import TestCase, override_settings

from allocate.services import run_allocation
from catalog.models import RegistrationPeriod
from recommend.models import Recommendation


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V3CoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()

    def test_student_home_computes_recommendations_and_journey(self):
        """Dữ liệu seed chưa chạy recommend_all: mở trang chủ là có Top gợi ý, hành trình đủ 4 mục."""
        self.assertFalse(Recommendation.objects.exists())
        self.client.login(username="sv001", password="123456")
        resp = self.client.get("/trang-chu/")
        self.assertTrue(resp.context["recommendations"])
        self.assertEqual([s["label"] for s in resp.context["journey"]][2:], ["Nguyện vọng", "Kết quả phân công"])
        self.assertEqual(resp.context["journey"][0]["state"], "done")

    def test_journey_after_publish_is_all_done(self):
        RegistrationPeriod.objects.update(status=RegistrationPeriod.Status.PUBLISHED)
        self.client.login(username="sv001", password="123456")
        journey = self.client.get("/trang-chu/").context["journey"]
        self.assertEqual({s["state"] for s in journey[2:]}, {"done"})
        self.assertEqual(journey[2]["note"], "Đã nộp · chỉ xem")

    def test_preferences_readonly_when_no_open_period(self):
        """Đợt đã đóng: SV vẫn xem lại nguyện vọng đã nộp (không còn trang trống)."""
        RegistrationPeriod.objects.update(status=RegistrationPeriod.Status.CLOSED)
        self.client.login(username="sv001", password="123456")
        ctx = self.client.get("/nguyen-vong/").context
        self.assertIsNone(ctx["period"])
        self.assertEqual(ctx["last_period"], self.period)
        self.assertEqual([row["pref"].rank for row in ctx["submitted"]], [1, 2, 3][: len(ctx["submitted"])])
        self.assertTrue(ctx["submitted"])

    def test_allocation_table_search_filter_and_paging(self):
        run_allocation(self.period, algorithm="GREEDY")
        self.client.login(username="khoa01", password="123456")
        ctx = self.client.get("/khoa/phan-cong/?per_page=10").context
        self.assertEqual(ctx["total_count"], 12)
        self.assertEqual(len(ctx["page_obj"]), 10)
        self.assertEqual(ctx["page_obj"].paginator.num_pages, 2)
        one = self.client.get("/khoa/phan-cong/?q=20230001").context
        self.assertEqual([a.student.student_code for a in one["allocations"]], ["20230001"])
        assigned = self.client.get("/khoa/phan-cong/?status=assigned").context["allocations"]
        self.assertTrue(all(a.topic_id for a in assigned))
        high = self.client.get("/khoa/phan-cong/?score_min=50").context["allocations"]
        self.assertTrue(all(a.match_score >= 50 for a in high))


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V34CoreTests(TestCase):
    """Phán quyết ATLAS V3.4: ngăn kéo tải riêng, điều kiện có cấu trúc, công bố có chặn, lý do từ chối 5–500."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()

    def test_eligibility_reasons_agree_with_eligible(self):
        from catalog.models import Student, Topic
        from recommend.engine import Profile, eligibility_reasons, eligible

        for st in Student.objects.all()[:5]:
            p = Profile(st)
            for t in Topic.objects.all():
                self.assertEqual(eligible(p, t)[0], all(r["ok"] for r in eligibility_reasons(p, t)))

    def test_student_drawer_fragment(self):
        from catalog.models import Student

        run_allocation(self.period, algorithm="GREEDY")
        st = Student.objects.get(user__username="sv001")
        url = f"/khoa/phan-cong/{self.period.pk}/sinh-vien/{st.pk}/"
        self.client.login(username="sv001", password="123456")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.login(username="khoa01", password="123456")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "<html")
        self.assertEqual(len(resp.context["prefs"]), st.preferences.count())

    def test_publish_refused_without_allocations_and_twice(self):
        self.client.login(username="khoa01", password="123456")
        self.client.post("/khoa/phan-cong/", {"action": "publish", "period_id": self.period.pk})
        self.period.refresh_from_db()
        self.assertNotEqual(self.period.status, RegistrationPeriod.Status.PUBLISHED)
        run_allocation(self.period, algorithm="GREEDY")
        self.client.post(f"/khoa/phan-cong/?period_id={self.period.pk}", {"action": "publish"})
        self.period.refresh_from_db()
        self.assertEqual(self.period.status, RegistrationPeriod.Status.PUBLISHED)

    def test_reject_reason_max_length(self):
        from catalog.models import Preference

        pref = Preference.objects.select_related("topic__lecturer__user").first()
        self.client.force_login(pref.topic.lecturer.user)
        url = f"/de-tai/{pref.topic.pk}/dang-ky/"
        self.client.post(url, {"preference_id": pref.pk, "action": "reject", "reason": "x" * 501})
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.PENDING)
        self.client.post(url, {"preference_id": pref.pk, "action": "reject", "reason": "Thiếu kỹ năng bắt buộc."})
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.REJECTED)


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V34DashboardTests(TestCase):
    def test_unassigned_count_shown(self):
        from allocate.models import Allocation

        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        period = RegistrationPeriod.objects.get()
        run_allocation(period, algorithm="GREEDY")
        self.client.login(username="khoa01", password="123456")
        m = self.client.get("/khoa/phan-cong/").context["metrics"]
        self.assertEqual(m["unassigned_count"], Allocation.objects.filter(period=period, topic__isnull=True).count())


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V35BackendTests(TestCase):
    """Chốt 14/10: nộp nguyện vọng 2 bước, mã đề tài tự sinh, nhận xét GV, nhập Excel 2 bước, tab điều kiện."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)

    def test_topic_code_autogenerated(self):
        from catalog.models import Topic

        codes = list(Topic.objects.values_list("code", flat=True))
        self.assertTrue(all(c and c.startswith("DT-") for c in codes))
        self.assertEqual(len(codes), len(set(codes)))

    def test_draft_hidden_from_lecturer_and_allocation_until_submitted(self):
        from allocate.services import _prepare_solver_data
        from catalog.models import Preference, Student

        st = Student.objects.get(user__username="sv001")
        period = RegistrationPeriod.objects.get()
        Preference.objects.filter(student=st).delete()
        self.client.login(username="sv001", password="123456")
        options = self.client.get("/nguyen-vong/").context["form"].fields["nv1"].queryset
        topic = options.first()
        self.client.post("/nguyen-vong/", {"nv1": topic.pk, "action": "draft"})
        pref = Preference.objects.get(student=st)
        self.assertFalse(pref.submitted)
        prefs, *_ = _prepare_solver_data(period, [st])
        self.assertEqual(prefs[st.id], [])
        self.client.force_login(topic.lecturer.user)
        rows = self.client.get(f"/de-tai/{topic.pk}/dang-ky/").context["rows"]
        self.assertNotIn(st.pk, [r["pref"].student_id for r in rows])
        self.client.login(username="sv001", password="123456")
        self.client.post("/nguyen-vong/", {"nv1": topic.pk, "action": "submit"})
        pref = Preference.objects.get(student=st)
        self.assertTrue(pref.submitted)
        self.assertIsNotNone(pref.submitted_at)
        self.client.post("/nguyen-vong/", {"action": "withdraw"})
        self.assertFalse(Preference.objects.get(student=st).submitted)

    def test_lecturer_note_saved_with_review(self):
        from catalog.models import Preference

        pref = Preference.objects.select_related("topic__lecturer__user").first()
        self.client.force_login(pref.topic.lecturer.user)
        self.client.post(
            f"/de-tai/{pref.topic.pk}/dang-ky/",
            {"preference_id": pref.pk, "action": "accept", "note": "Hồ sơ tốt, cần bổ sung Git."},
        )
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.ACCEPTED)
        self.assertEqual(pref.lecturer_note, "Hồ sơ tốt, cần bổ sung Git.")

    def test_excel_import_two_steps(self):
        import io

        from catalog.importer import create_sample_excel
        from catalog.models import Student

        before = Student.objects.count()
        self.client.login(username="khoa01", password="123456")
        f = io.BytesIO(create_sample_excel())
        f.name = "mau.xlsx"
        r = self.client.post("/khoa/nhap-excel/", {"file": f, "action": "check"})
        self.assertTrue(r.context["result"]["ok"])
        self.assertTrue(r.context["result"]["pending"])
        self.assertEqual(Student.objects.count(), before)  # bước kiểm tra chưa ghi gì
        r = self.client.post("/khoa/nhap-excel/", {"action": "confirm"})
        self.assertTrue(r.context["result"]["ok"])
        self.assertGreater(Student.objects.count(), before)
        r = self.client.post("/khoa/nhap-excel/", {"action": "confirm"})  # xác nhận lần 2: không còn tệp chờ
        self.assertIsNone(r.context["result"])

    def test_topic_list_eligibility_tabs(self):
        self.client.login(username="sv001", password="123456")
        ctx = self.client.get("/danh-sach-de-tai/").context
        counts = ctx["tab_counts"]
        self.assertEqual(counts["ok"] + counts["no"], counts["all"])
        ok_page = self.client.get("/danh-sach-de-tai/?dk=1&per_page=50").context["page_obj"]
        self.assertEqual(len(ok_page), counts["ok"])
        self.assertTrue(all(not t.ineligible_reason for t in ok_page))
        self.assertEqual(self.client.get("/danh-sach-de-tai/?sort=score").status_code, 200)

    def test_profile_completeness(self):
        self.client.login(username="sv001", password="123456")
        ctx = self.client.get("/ho-so/").context
        self.assertIn(ctx["completeness"], (0, 25, 50, 75, 100))
        self.assertEqual(len(ctx["completeness_items"]), 4)


class V37CoreTests(TestCase):
    """Nghiệm thu 15/10: SV tự sửa email/SĐT; trang chủ GV liệt kê từng SV chờ duyệt (thấy tên SV)."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)

    def _profile_post(self, **extra):
        ctx = self.client.get("/ho-so/").context
        data = {}
        data["interest-shown"] = "1"
        data["interest-picked"] = [str(f) for f in ctx["interest_form"].initial["picked"]]
        for fs in (ctx["skill_formset"],):
            mf = fs.management_form
            data.update({f"{fs.prefix}-{k}": v for k, v in mf.initial.items()})
            for form in fs.forms:
                data.update({form.add_prefix(k): v for k, v in form.initial.items() if v is not None})
                if form.instance.pk:
                    data[form.add_prefix("id")] = form.instance.pk
        data["about"] = ctx["student"].about
        data.update(extra)
        return self.client.post("/ho-so/", data)

    def test_student_edits_contact(self):
        from catalog.models import Student

        self.client.login(username="sv001", password="123456")
        r = self._profile_post(email="sv001@truong.edu.vn", phone="0912 345 678")
        self.assertEqual(r.status_code, 302)
        st = Student.objects.select_related("user").get(user__username="sv001")
        self.assertEqual((st.user.email, st.phone), ("sv001@truong.edu.vn", "0912345678"))

    def test_bad_phone_rejected_and_old_page_keeps_contact(self):
        from catalog.models import Student

        self.client.login(username="sv001", password="123456")
        self._profile_post(email="a@b.vn", phone="0912345678")
        r = self._profile_post(email="a@b.vn", phone="12ab")
        self.assertEqual(r.status_code, 200)
        self.assertIn("phone", r.context["contact_form"].errors)
        data_without_contact = self._profile_post()  # biểu mẫu không có ô liên hệ → giữ nguyên
        self.assertEqual(data_without_contact.status_code, 302)
        self.assertEqual(Student.objects.get(user__username="sv001").phone, "0912345678")

    def test_lecturer_home_lists_pending_students(self):
        from catalog.models import Preference

        pref = (
            Preference.objects.filter(submitted=True, status=Preference.Status.PENDING)
            .select_related("topic__lecturer__user", "student__user")
            .first()
        )
        self.client.force_login(pref.topic.lecturer.user)
        ctx = self.client.get("/trang-chu/").context
        self.assertIn(pref.pk, [r["pref"].pk for r in ctx["review_rows"]])
        code = pref.student.student_code
        rows = self.client.get("/trang-chu/", {"q": code}).context["review_rows"]
        self.assertTrue(rows and all(r["pref"].student.student_code == code for r in rows))
        rows = self.client.get("/trang-chu/", {"tt": "dong-y"}).context["review_rows"]
        self.assertTrue(all(r["pref"].status == Preference.Status.ACCEPTED for r in rows))

    def test_interest_checkboxes_max_three_keep_levels(self):
        from catalog.models import Field, Student

        self.client.login(username="sv001", password="123456")
        st = Student.objects.get(user__username="sv001")
        old = dict(st.interests.values_list("field_id", "level"))
        keep = next(iter(old))
        new = list(Field.objects.exclude(pk__in=old).values_list("pk", flat=True)[:3])
        r = self._profile_post(**{"interest-picked": [keep, *new]})
        self.assertIn("picked", r.context["interest_form"].errors)  # 4 lĩnh vực → bị chặn
        r = self._profile_post(**{"interest-picked": [keep, new[0]]})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(dict(st.interests.values_list("field_id", "level")), {keep: old[keep], new[0]: 3})

    def test_condition_checklist_on_three_pages(self):
        from catalog.models import Preference

        pref = (
            Preference.objects.filter(submitted=True).select_related("topic__lecturer__user", "student__user").first()
        )
        self.client.force_login(pref.student.user)
        items = self.client.get(f"/danh-sach-de-tai/{pref.topic_id}/").context["checklist"]
        labels = [i["label"] for i in items]
        self.assertTrue(labels[0].startswith("GPA") and "Kỹ năng phù hợp" in labels and "Chỉ tiêu còn chỗ" in labels)
        self.assertTrue(all(i["state"] in ("ok", "warn", "fail") for i in items))
        rows = self.client.get("/nguyen-vong/").context["pref_rows"]
        self.assertTrue(all(r["checklist"] for r in rows))
        self.client.force_login(pref.topic.lecturer.user)
        rows = self.client.get(f"/de-tai/{pref.topic_id}/dang-ky/").context["rows"]
        self.assertTrue(all(r["checklist"] for r in rows))

    def test_reason_points_and_csv_items(self):
        from catalog.templatetags.atlas_tags import csv_items, reason_points

        text = "Phù hợp vì bạn đáp ứng kỹ năng, đề tài thuộc lĩnh vực bạn quan tâm. Cần bổ sung: Kiểm thử phần mềm"
        self.assertEqual(
            reason_points(text),
            ["Bạn đáp ứng kỹ năng", "Đề tài thuộc lĩnh vực bạn quan tâm", "Cần bổ sung: Kiểm thử phần mềm"],
        )
        self.assertEqual(reason_points(""), [])
        self.assertEqual(csv_items("Flutter, Firebase; REST API,"), ["Flutter", "Firebase", "REST API"])

    def test_result_page_and_faculty_home_data(self):
        from allocate.services import publish_allocations, run_allocation
        from catalog.models import Student

        period = RegistrationPeriod.objects.get()
        period.status = RegistrationPeriod.Status.CLOSED
        period.save()
        run_allocation(period)
        publish_allocations(period, user=None)
        st = Student.objects.filter(allocation__topic__isnull=False).first()
        self.client.force_login(st.user)
        ctx = self.client.get("/ket-qua/").context
        self.assertIsNotNone(ctx["published_at"])
        self.assertEqual(len(ctx["journey"]), 4)
        self.assertTrue(ctx["preferences"].exists())
        self.client.login(username="khoa01", password="123456")
        ctx = self.client.get("/trang-chu/").context
        self.assertEqual(ctx["n_lecturers"], 4)
        self.assertGreater(ctx["n_with_pref"], 0)

    def test_registrations_page_keeps_drawer_deeplink(self):
        from catalog.models import Preference

        pref = Preference.objects.filter(submitted=True).select_related("topic__lecturer__user")[0]
        self.client.force_login(pref.topic.lecturer.user)
        html = self.client.get(f"/de-tai/{pref.topic_id}/dang-ky/?mo={pref.pk}").content.decode()
        self.assertIn('get("mo")', html)
        self.assertIn(f'id="atStudent{pref.pk}"', html)

    def test_published_results_cannot_be_overwritten(self):
        from allocate.models import Allocation
        from allocate.services import publish_allocations, run_allocation

        period = RegistrationPeriod.objects.get()
        period.status = RegistrationPeriod.Status.CLOSED
        period.save()
        run_allocation(period)
        publish_allocations(period, user=None)
        before = list(Allocation.objects.filter(period=period).values_list("student_id", "topic_id", "status"))
        self.client.login(username="khoa01", password="123456")
        for action in ("run_ilp", "run_greedy"):
            r = self.client.post(f"/khoa/phan-cong/?period_id={period.pk}", {"action": action}, follow=True)
            self.assertContains(r, "đã công bố")
        st = Allocation.objects.filter(period=period).first().student
        self.client.post(
            f"/khoa/phan-cong/?period_id={period.pk}",
            {"action": "manual_assign", "student_id": st.pk, "topic_id": "none"},
        )
        period.refresh_from_db()
        self.assertEqual(period.status, RegistrationPeriod.Status.PUBLISHED)
        after = list(Allocation.objects.filter(period=period).values_list("student_id", "topic_id", "status"))
        self.assertEqual(before, after)

    def test_bad_query_params_never_500(self):
        cases = {
            "sv001": [
                "/danh-sach-de-tai/?per_page=xyz&field=x&lecturer=y&difficulty=z&page=abc",
                "/ket-qua/?period_id=abc",
            ],
            "khoa01": [
                "/khoa/phan-cong/?period_id=abc&page=x&per_page=y&score_min=z",
                "/khoa/thong-ke/?period_id=abc",
                "/ho-so-giang-vien/?lecturer_id=abc",
            ],
        }
        for user, urls in cases.items():
            self.client.login(username=user, password="123456")
            for url in urls:
                self.assertIn(self.client.get(url).status_code, (200, 302, 404), url)
