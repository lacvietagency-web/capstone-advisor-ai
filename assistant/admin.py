from django.contrib import admin

from .models import ChatLog


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "role", "question", "mode", "model", "ms")
    list_filter = ("role", "mode")
    search_fields = ("question", "answer")
    readonly_fields = [f.name for f in ChatLog._meta.fields]
