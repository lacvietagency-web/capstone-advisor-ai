from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AppUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Vai trò trong hệ thống", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Vai trò trong hệ thống", {"fields": ("role",)}),)
