from django.contrib import admin

from .models import Allocation


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ("period", "student", "topic", "preference_rank", "match_score", "status", "source")
    list_filter = ("period", "status", "source", "preference_rank")
