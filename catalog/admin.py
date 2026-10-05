"""Trang quản trị cho Khoa: Django tự sinh màn hình thêm/sửa/xoá/tìm kiếm cho mọi bảng đăng ký ở đây.

Hỗ trợ action và màn hình nhập dữ liệu hàng loạt từ Excel (UC15).
Công thức tổng hợp bản ghi:
    N_tong = N_SV + N_GV + N_DeTai + N_KyNang
"""

from pathlib import Path

from django.contrib import admin, messages
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .importer import create_sample_excel, import_excel_data
from .models import (
    AuditLog,
    Course,
    Field,
    Lecturer,
    Major,
    Preference,
    RegistrationPeriod,
    Skill,
    Student,
    StudentCourseResult,
    StudentInterest,
    StudentSkill,
    Topic,
    TopicPrerequisite,
    TopicSkill,
)

admin.site.site_header = "Capstone Advisor AI — Quản trị Khoa"
admin.site.site_title = "Capstone Advisor AI"


def download_sample_excel_response() -> HttpResponse:
    """Trả về phản hồi tải tệp Excel mẫu catalog/mau_nhap_lieu.xlsx."""
    sample_path = Path(__file__).resolve().parent / "mau_nhap_lieu.xlsx"
    if not sample_path.exists():
        create_sample_excel(sample_path)
    return FileResponse(
        open(sample_path, "rb"),
        as_attachment=True,
        filename="mau_nhap_lieu.xlsx",
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def handle_admin_excel_import(modeladmin, request, queryset=None) -> HttpResponse:
    """Xử lý yêu cầu nhập dữ liệu Excel từ action hoặc màn hình tải lên trong trang quản trị.

    Đảm bảo tính nguyên tử qua transaction:
    Nếu có bất kỳ dòng nào lỗi, không có dữ liệu nào được lưu vào CSDL.
    """
    file_obj = request.FILES.get("excel_file") or request.FILES.get("file")
    changelist_url = reverse(f"admin:{modeladmin.opts.app_label}_{modeladmin.opts.model_name}_changelist")

    if request.method == "POST" and file_obj:
        success, errors, stats = import_excel_data(file_obj)
        if success:
            AuditLog.objects.create(
                user=request.user,
                action="import_excel",
                entity="Catalog",
                entity_id="admin_action",
                detail=stats,
            )
            msg = (
                f"Nhập dữ liệu thành công từ Excel: {stats['students']} sinh viên, "
                f"{stats['lecturers']} giảng viên, {stats['topics']} đề tài, {stats['skills']} kỹ năng."
            )
            modeladmin.message_user(request, msg, messages.SUCCESS)
        else:
            err_summary = "Lỗi nhập Excel (toàn bộ thay đổi đã bị hủy bỏ):\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                err_summary += f"\n... và {len(errors) - 10} lỗi khác."
            modeladmin.message_user(request, err_summary, messages.ERROR)
        return HttpResponseRedirect(changelist_url)

    context = {
        **modeladmin.admin_site.each_context(request),
        "opts": modeladmin.opts,
        "title": "Nhập dữ liệu từ Excel (.xlsx)",
        "queryset": queryset,
        "is_action": queryset is not None,
    }
    return render(request, "admin/catalog/import_excel.html", context)


class ExcelImportAdminMixin:
    """Mixin cung cấp action và view nhập Excel cho ModelAdmin."""

    actions = ["import_excel"]

    @admin.action(description="Nhập dữ liệu từ Excel (.xlsx)")
    def import_excel(self, request, queryset=None):
        """Action quản trị cho phép tải lên file Excel để nhập dữ liệu."""
        return handle_admin_excel_import(self, request, queryset)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-excel/",
                self.admin_site.admin_view(self.import_excel_view),
                name=f"{self.opts.app_label}_{self.opts.model_name}_import_excel",
            ),
            path(
                "mau-nhap-lieu/",
                self.admin_site.admin_view(self.download_sample_excel_view),
                name=f"{self.opts.app_label}_{self.opts.model_name}_sample_excel",
            ),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        return handle_admin_excel_import(self, request)

    def download_sample_excel_view(self, request):
        return download_sample_excel_response()


for model in (Major, Field, Course):
    admin.site.register(model)


@admin.register(Skill)
class SkillAdmin(ExcelImportAdminMixin, admin.ModelAdmin):
    list_display = ("name", "field")
    list_filter = ("field",)
    search_fields = ("name",)


class StudentSkillInline(admin.TabularInline):
    model = StudentSkill
    extra = 0


class StudentInterestInline(admin.TabularInline):
    model = StudentInterest
    extra = 0


class StudentCourseInline(admin.TabularInline):
    model = StudentCourseResult
    extra = 0


@admin.register(Student)
class StudentAdmin(ExcelImportAdminMixin, admin.ModelAdmin):
    list_display = ("student_code", "user", "major", "gpa")
    list_filter = ("major",)
    search_fields = ("student_code", "user__first_name", "user__last_name")
    inlines = [StudentSkillInline, StudentInterestInline, StudentCourseInline]


@admin.register(Lecturer)
class LecturerAdmin(ExcelImportAdminMixin, admin.ModelAdmin):
    list_display = ("user", "department", "max_students")
    filter_horizontal = ("fields",)


class TopicSkillInline(admin.TabularInline):
    model = TopicSkill
    extra = 0


class TopicPrereqInline(admin.TabularInline):
    model = TopicPrerequisite
    extra = 0


@admin.register(Topic)
class TopicAdmin(ExcelImportAdminMixin, admin.ModelAdmin):
    list_display = ("title", "lecturer", "difficulty", "capacity", "min_gpa", "status")
    list_filter = ("status", "difficulty", "fields", "lecturer")
    search_fields = ("title", "description")
    filter_horizontal = ("fields",)
    inlines = [TopicSkillInline, TopicPrereqInline]


@admin.register(RegistrationPeriod)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "start_at", "end_at", "status")


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("student", "rank", "topic", "status", "period", "created_at")
    list_filter = ("period", "rank", "status")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("at", "user", "action", "entity", "entity_id")
    readonly_fields = ("at", "user", "action", "entity", "entity_id", "detail")
