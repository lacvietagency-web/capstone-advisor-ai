"""Trang quản trị cho Khoa: Django tự sinh màn hình thêm/sửa/xoá/tìm kiếm cho mọi bảng đăng ký ở đây."""

from django.contrib import admin

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

for model in (Major, Field, Course):
    admin.site.register(model)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
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
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_code", "user", "major", "gpa")
    list_filter = ("major",)
    search_fields = ("student_code", "user__first_name", "user__last_name")
    inlines = [StudentSkillInline, StudentInterestInline, StudentCourseInline]


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "max_students")
    filter_horizontal = ("fields",)


class TopicSkillInline(admin.TabularInline):
    model = TopicSkill
    extra = 0


class TopicPrereqInline(admin.TabularInline):
    model = TopicPrerequisite
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
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
    list_display = ("student", "rank", "topic", "period", "created_at")
    list_filter = ("period", "rank")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("at", "user", "action", "entity", "entity_id")
    readonly_fields = ("at", "user", "action", "entity", "entity_id", "detail")
