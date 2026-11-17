from django.contrib import admin

from .models import GopY


@admin.register(GopY)
class GopYAdmin(admin.ModelAdmin):
    list_display = ("pk", "ten", "created_at")
    readonly_fields = ("ten", "noi_dung", "created_at")
