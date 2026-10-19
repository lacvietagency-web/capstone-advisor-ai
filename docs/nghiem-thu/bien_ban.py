"""Dựng biên bản 84 ca (docs/KICH-BAN-KIEM-THU.md) từ kết quả chạy THẬT:
  - ca máy chủ → chạy đúng các test Django được ánh xạ, ca ĐẠT khi mọi test của ca đạt;
  - ca trình duyệt → đọc <thư mục>/ket-qua.json do browser_checks.py ghi.
Ca không có bằng chứng nào → "Chưa kiểm chứng" (không bao giờ tự ghi Đạt).

  python docs/nghiem-thu/bien_ban.py <ket-qua-trinh-duyet.json> docs/nghiem-thu/BIEN-BAN-84-CA.md
"""

import io
import json
import os
import re
import sys
import unittest
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
os.chdir(REPO)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("RECOMMEND_SEMANTIC", "0")
os.environ.setdefault("RECOMMEND_LLM", "0")

AC = "accounts.tests_acceptance_cases.AcceptanceCases."
MX = "accounts.tests_acceptance_matrix.AcceptanceAuthzMatrix."
V3 = "accounts.tests_v3."
CT = "catalog.tests."
AL = "allocate.tests."
PR = "allocate.tests_acceptance_props.AllocationProperties."
RP = "recommend.tests_acceptance_props."
FI = "catalog.tests_acceptance_files.MaliciousExcelUploads."

# Mã ca → test Django làm bằng chứng (đọc mô tả từng test trước khi ánh xạ, 20/10/2026)
SERVER = {
    "A01": [AC + "test_a01_login_returns_to_requested_page", MX + "test_get_matrix"],
    "A02": [AC + "test_a02_wrong_login_same_message_keeps_username"],
    "A05": ["accounts.tests.RoleAccessTests.test_student_home", "accounts.tests.RoleAccessTests.test_lecturer_home",
            "accounts.tests.RoleAccessTests.test_admin_home"],
    "A06": ["accounts.tests.PasswordChangeTests.test_password_change_successful_flow",
            "accounts.tests.PasswordChangeTests.test_password_change_wrong_old_password",
            "accounts.tests.PasswordChangeTests.test_password_change_mismatched_new_passwords",
            "accounts.tests.PasswordChangeTests.test_password_change_weak_password_rejected",
            AC + "test_a06_password_similar_to_username_rejected"],
    "A07": [AC + "test_a07_logout_ends_session"],
    "A08": [MX + "test_get_matrix", MX + "test_post_matrix_never_changes_data_for_wrong_role"],
    "A09": [MX + "test_get_matrix"],
    "A10": [MX + "test_get_matrix", AC + "test_a10_other_lecturer_cannot_review_by_post",
            CT + "BusinessFlowTests.test_only_topic_owner_can_manage_registrations"],
    "A11": [MX + "test_get_matrix"],
    "A12": [CT + "CoreMosaicTests.test_403_and_404_pages"],
    "A13": [CT + "TopicPermissionAndDetailTests.test_draft_topic_permission", AC + "test_a13_closed_topic_viewable_without_register"],
    "S01": [V3 + "V3CoreTests.test_student_home_computes_recommendations_and_journey"],
    "S02": [V3 + "V35BackendTests.test_profile_completeness"],
    "S03": [V3 + "V37CoreTests.test_student_edits_contact", AC + "test_s03_readonly_fields_cannot_be_tampered"],
    "S04": [V3 + "V37CoreTests.test_student_edits_contact", V3 + "V37CoreTests.test_bad_phone_rejected_and_old_page_keeps_contact"],
    "S05": [CT + "CoreMosaicTests.test_duplicate_skill_rows_show_clear_error", CT + "BusinessFlowTests.test_student_profile_save_recomputes"],
    "S06": [V3 + "V37CoreTests.test_interest_checkboxes_max_three_keep_levels"],
    "S07": [V3 + "V37CoreTests.test_interest_checkboxes_max_three_keep_levels", CT + "BusinessFlowTests.test_student_profile_save_recomputes"],
    "S08": [AC + "test_s08_about_length_and_script_escaped"],
    "S09": [V3 + "V35BackendTests.test_topic_list_eligibility_tabs"],
    "S10": [CT + "TopicFilterTests.test_filter_by_field", CT + "TopicFilterTests.test_filter_by_lecturer",
            CT + "TopicFilterTests.test_filter_by_difficulty", CT + "TopicFilterTests.test_search_by_title",
            CT + "TopicFilterTests.test_combined_filters", CT + "TopicFilterTests.test_pagination",
            CT + "CatalogServiceTests.test_filter_topics_service_no_matches"],
    "S11": [AC + "test_s11_special_characters_in_search_never_500", V3 + "V37CoreTests.test_bad_query_params_never_500"],
    "S12": [CT + "TopicPermissionAndDetailTests.test_student_sees_topic_detail_elements", V3 + "V37CoreTests.test_condition_checklist_on_three_pages"],
    "S13": [CT + "TopicPermissionAndDetailTests.test_ineligible_topic_hides_register_and_shows_reason"],
    "S14": [V3 + "V35BackendTests.test_draft_hidden_from_lecturer_and_allocation_until_submitted"],
    "S15": [V3 + "V35BackendTests.test_draft_hidden_from_lecturer_and_allocation_until_submitted"],
    "S16": [CT + "BusinessFlowTests.test_student_preferences_no_duplicates"],
    "S17": [CT + "BusinessFlowTests.test_resaving_preferences_keeps_lecturer_decision", V3 + "V39AcceptGuardTests.test_withdraw_keeps_seat_no_overbooking"],
    "S18": [AC + "test_s18_register_when_three_preferences_keeps_old_ones"],
    "S19": [V3 + "V3CoreTests.test_preferences_readonly_when_no_open_period", V3 + "V39DeadlineTests.test_after_deadline_student_cannot_change"],
    "S20": [V3 + "V35BackendTests.test_lecturer_note_saved_with_review"],
    "S21": [AL + "StudentAllocationResultTests.test_when_period_not_published_shows_waiting_status",
            AL + "StudentAllocationResultTests.test_service_when_no_period_exists"],
    "S22": [AL + "StudentAllocationResultTests.test_when_period_published_shows_assigned_details", V3 + "V37CoreTests.test_result_page_and_faculty_home_data"],
    "S23": [AL + "StudentAllocationResultTests.test_when_period_published_but_student_unassigned"],
    "S24": [AL + "StudentAllocationResultTests.test_filter_by_period_id", V3 + "V37CoreTests.test_bad_query_params_never_500"],
    "L01": ["accounts.tests.LecturerHomeDashboardTests.test_lecturer_dashboard_kpi_metrics", V3 + "V37CoreTests.test_lecturer_home_lists_pending_students"],
    "L02": [V3 + "V37CoreTests.test_lecturer_home_lists_pending_students"],
    "L03": [V3 + "V37CoreTests.test_registrations_page_keeps_drawer_deeplink"],
    "L04": [AC + "test_l04_my_topics_lists_only_own"],
    "L05": [V3 + "V37CoreTests.test_topic_form_rejects_bad_gpa_capacity_weight", CT + "CoreMosaicTests.test_duplicate_skill_rows_show_clear_error"],
    "L06": [CT + "BusinessFlowTests.test_lecturer_creates_topic", V3 + "V35BackendTests.test_topic_code_autogenerated"],
    "L07": [AC + "test_l07_editing_description_bumps_version"],
    "L08": [AC + "test_l08_registrations_default_to_pending"],
    "L09": [V3 + "V34CoreTests.test_student_drawer_fragment"],
    "L10": [CT + "BusinessFlowTests.test_lecturer_registrations_view_and_accept", V3 + "V35BackendTests.test_lecturer_note_saved_with_review"],
    "L11": [CT + "BusinessFlowTests.test_lecturer_registrations_reject", V3 + "V34CoreTests.test_reject_reason_max_length",
            AL + "AllocationFlowTests.test_rejected_preference_not_allocated_ilp"],
    "L12": [CT + "BusinessFlowTests.test_lecturer_updates_profile_when_open", CT + "BusinessFlowTests.test_lecturer_cannot_update_quota_when_period_closed",
            AC + "test_l12_lecturer_phone_never_shown_to_students"],
    "L13": [V3 + "V39SupervisingCountTests.test_after_publish_only_official_allocations_count"],
    "K01": [V3 + "V37CoreTests.test_result_page_and_faculty_home_data", "accounts.tests.RoleAccessTests.test_admin_home"],
    "K02": [CT + "ExcelImportTests.test_create_sample_excel_file", MX + "test_get_matrix"],
    "K03": [CT + "ExcelImportTests.test_invalid_file_format", CT + "ExcelImportTests.test_invalid_gpa_row_error_and_transaction_rollback",
            CT + "ExcelImportTests.test_invalid_email_and_missing_fields_row_errors", FI + "test_bad_files_through_faculty_upload_page",
            FI + "test_xml_bomb_rejected_quickly", FI + "test_zip_bomb_under_upload_limit_rejected_before_parsing"],
    "K04": [V3 + "V35BackendTests.test_excel_import_two_steps"],
    "K05": [V3 + "V35BackendTests.test_excel_import_two_steps", V3 + "V39ImportCaseTests.test_code_clash_differs_only_by_case"],
    "K06": [AL + "AllocationFlowTests.test_run_ilp_and_greedy_flow", AL + "AllocationFlowTests.test_filter_unassigned_and_metrics_display"],
    "K07": [PR + "test_ilp_and_greedy_always_feasible", AL + "AllocationFlowTests.test_rejected_preference_not_allocated_ilp",
            AL + "AllocationFlowTests.test_rejected_preference_not_allocated_greedy", AL + "HardFilterAllocationTests.test_ineligible_preference_never_allocated"],
    "K08": [V3 + "V3CoreTests.test_allocation_table_search_filter_and_paging"],
    "K09": [AL + "AllocationFlowTests.test_phase2_suggestions_and_manual_assign", V3 + "V37CoreTests.test_manual_assign_respects_capacity_and_quota"],
    "K10": [AL + "AllocationFlowTests.test_publish_allocations_flow"],
    "K11": [V3 + "V37CoreTests.test_published_results_cannot_be_overwritten", V3 + "V39AcceptGuardTests.test_locked_after_publish"],
    "K12": [V3 + "V34CoreTests.test_publish_refused_without_allocations_and_twice"],
    "K13": ["reports.tests.FacultyStatisticsViewTestCase.test_faculty_admin_can_access_dashboard"],
    "K14": [AC + "test_k14_admin_site_only_for_faculty"],
    "B01": ["recommend.tests.EngineTests.test_hard_filter_gpa_and_mandatory_skill", CT + "BusinessFlowTests.test_ineligible_topic_is_rejected_with_reason"],
    "B02": ["recommend.tests.EngineTests.test_m1_skill", RP + "ScoreProperties.test_m1_in_range_and_full_when_all_met"],
    "B03": ["recommend.tests.EngineTests.test_m3_field", RP + "ScoreProperties.test_m3_in_range"],
    "B04": [RP + "ScoreProperties.test_final_score_between_component_scores", "recommend.tests_llm.LLMScoringTests.test_json_error_yields_none_and_rebalances_weights"],
    "B05": ["recommend.tests.AHPTests.test_perfect_consistency_eigen_method", "recommend.tests.AHPTests.test_inconsistent_matrix_rejected_by_model",
            "recommend.tests.AHPTests.test_weightset_single_active", RP + "AHPProperties.test_consistent_matrix_recovers_weights"],
    "B06": [CT + "BusinessFlowTests.test_student_profile_save_recomputes"],
    "B07": [V3 + "V39HeldSeatTests.test_holder_sees_accepted_not_full", V3 + "V39AcceptGuardTests.test_withdraw_keeps_seat_no_overbooking"],
    "B08": [V3 + "V35BackendTests.test_topic_code_autogenerated"],
    "B09": [CT + "ExcelImportTests.test_invalid_gpa_row_error_and_transaction_rollback", CT + "ExcelImportTests.test_detai_missing_lecturer_rollback"],
    "B10": [AC + "test_b10_audit_log_for_main_actions"],
    "B12": [AL + "CommandTests.test_allocate_period_saves_drafts", AC + "test_b12_allocate_period_refuses_published"],
}
# Use case chỉ làm qua trang quản trị: test riêng, mã "UCxx" dùng trong ma trận truy vết bên dưới
SERVER.update({f"UC{n}": [AC + t] for n, t in (
    ("14", "test_uc14_faculty_moves_period_through_states_in_admin"),
    ("16", "test_uc16_faculty_adjusts_capacity_and_closes_topic_in_admin"),
    ("22", "test_uc22_audit_log_searchable_and_read_only"),
    ("23", "test_uc23_activate_weight_set_from_admin_keeps_one_active"))})
# Ma trận truy vết (kế hoạch #9): use case trong docs/USE-CASE.md → mã ca
TRACE = {
    "UC01": "A01 A02 A03 A05 A08 A09 A10 A11 K14", "UC02": "A07", "UC03": "A06", "UC04": "S03 S04 S05 S06 S07 S08 B06",
    "UC05": "S01 S02 B01 B02 B03 B04", "UC06": "S09 S10 S11 S12 S13 A12 A13", "UC07": "S14 S15 S16 S17 S18 S19 S20",
    "UC08": "S21 S22 S23 S24", "UC09": "L12 L13", "UC10": "L05 L06 B08", "UC11": "L04 L07",
    "UC12": "L09 L10 L11 B07 B09", "UC13": "L01 L02 L03 L08", "UC14": "UC14 S19 S21 K11", "UC15": "K02 K03 K04 K05",
    "UC16": "UC16 K14", "UC17": "K01 K13", "UC18": "K06 K07", "UC19": "K08 K09", "UC20": "K10 K11 K12",
    "UC21": "K13", "UC22": "UC22 B10", "UC23": "UC23 B05",
}
# Ca chỉ kiểm được trên trình duyệt → mã trong ket-qua.json của browser_checks.py
BROWSER = {"A03": ["A03"], "A04": ["A04"], "A14": ["A14"], "K10": ["K10"], "K13": ["K13"], "U01": ["U01", "G1"],
           "U02": ["U02"], "U03": ["U03"], "U04": ["AXE"], "U05": ["U05"], "U06": ["U06"], "U07": ["U07"]}
# Ca đo bằng công cụ riêng (ghi tay kết quả đo, có tệp bằng chứng)
# Đo ngày 20/10/2026, CSDL 1.000 SV / 60 GV / 300 đề tài, Locust 3 phút mỗi lượt, 0 lỗi (docs/nghiem-thu/locust/).
MEASURED = {"B11": "1 người: mọi trang 6–110 ms (Thống kê lần đầu 1,03 s, có bộ đệm 21 ms); Locust 50 người p95 390 ms "
                   "(runserver), 100 người p95 110 ms, 28,4 yêu cầu/s (gunicorn 8 tiến trình); 0 lỗi — docs/nghiem-thu/locust/"}


def run_tests(labels):
    import django
    from django.test.utils import get_runner
    from django.conf import settings

    django.setup()
    runner = get_runner(settings)(verbosity=0, interactive=False)
    suite = runner.build_suite(sorted(set(labels)))
    ran = {t.id() for t in _iter(suite)}  # lấy trước khi chạy: unittest dọn suite sau khi chạy xong
    runner.setup_test_environment()  # như manage.py test: ALLOWED_HOSTS "testserver", hộp thư giả…
    old = runner.setup_databases()
    try:
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    finally:
        runner.teardown_databases(old)
        runner.teardown_test_environment()
    bad = {t.id() for t, _ in result.failures + result.errors}
    for t, tb in (result.failures + result.errors)[:3]:
        print("LỖI", t.id(), tb.strip().splitlines()[-1][:200], file=sys.stderr)
    return ran, bad


def _iter(suite):
    for t in suite:
        yield from (_iter(t) if isinstance(t, unittest.TestSuite) else [t])


def main():
    browser = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 and Path(sys.argv[1]).exists() else []
    ran, bad = run_tests([t for ts in SERVER.values() for t in ts])
    spec = (REPO / "docs/KICH-BAN-KIEM-THU.md").read_text()
    cases = re.findall(r"^\| ([ASLKBU]\d{2}) \|(.+)$", spec, re.M)
    rows, tally, statuses = [], {}, {}
    for code in [c for c in SERVER if c.startswith("UC")]:
        statuses[code] = "Không đạt" if set(SERVER[code]) & bad else ("Đạt" if set(SERVER[code]) <= ran else "Chưa kiểm chứng")
    for code, rest in cases:
        cells = [c.strip() for c in rest.split("|") if c.strip()]
        what = cells[-2] if len(cells) >= 2 else cells[0]
        if code in SERVER:
            tests = SERVER[code]
            missing = [t for t in tests if t not in ran]
            failed = [t for t in tests if t in bad]
            status = "Chưa kiểm chứng" if missing else ("Không đạt" if failed else "Đạt")
            ev = f"{len(tests)} test tự động" + (f"; thiếu: {', '.join(m.split('.')[-1] for m in missing)}" if missing else "")
        elif code in BROWSER:
            hits = [r for r in browser if r["ma"] in BROWSER[code]]
            res = {r["ket_qua"] for r in hits}
            status = "Chưa kiểm chứng" if not hits or res & {"CHƯA KIỂM CHỨNG", "LỖI KỊCH BẢN"} else (
                "Không đạt" if "KHÔNG ĐẠT" in res else "Đạt")
            ev = "Trình duyệt: " + "; ".join(f"{r['trinh_duyet']} {r['ket_qua']}" for r in hits) if hits else "chưa chạy"
        elif code in MEASURED:
            status, ev = "Đạt", MEASURED[code]
        else:
            status, ev = "Chưa kiểm chứng", "chưa có bằng chứng"
        statuses[code] = status
        tally[status] = tally.get(status, 0) + 1
        rows.append(f"| {code} | {what[:90]} | {status} | {ev} |")
    out = [f"# Biên bản thực hiện 84 ca kiểm thử — Capstone Advisor AI\n\nNgày chạy: {datetime.now():%d/%m/%Y %H:%M}. "
          f"Nguồn: chạy lại {len(ran)} test tự động được ánh xạ (lỗi: {len(bad)}) + kết quả trình duyệt "
          f"({len(browser)} mục). Tổng hợp: " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())) + ".\n",
           "| Mã | Ca | Kết quả | Bằng chứng |", "|---|---|---|---|", *rows]
    names = dict(re.findall(r"^### (UC\d{2}): (.+)$", (REPO / "docs/USE-CASE.md").read_text(), re.M))
    out += ["\n## Ma trận truy vết use case ↔ ca kiểm thử\n",
            "Use case đạt khi MỌI ca ánh xạ đều đạt. Mã `UCxx` là test riêng cho thao tác qua trang quản trị `/quan-tri/`.\n",
            "| Use case | Tên | Ca kiểm thử | Kết quả |", "|---|---|---|---|"]
    for uc, codes in TRACE.items():
        res = {statuses.get(c, "Chưa kiểm chứng") for c in codes.split()}
        verdict = "Không đạt" if "Không đạt" in res else ("Chưa kiểm chứng" if res - {"Đạt"} else "Đạt")
        out.append(f"| {uc} | {names.get(uc, '')} | {', '.join(codes.split())} | {verdict} |")
    Path(sys.argv[2]).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(out[0].splitlines()[-1] if out else "")


if __name__ == "__main__":
    main()
