from django.contrib import admin, messages

from .models import LLMScore, Recommendation, WeightSet


@admin.register(WeightSet)
class WeightSetAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "cr", "weights_summary", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    actions = ["activate_weight_set"]

    @admin.display(description="Trọng số (skill / acad / field / sem / llm)")
    def weights_summary(self, obj):
        if not obj.weights:
            return "-"
        w = obj.weights
        return (
            f"{w.get('skill', 0):.2f} / {w.get('academic', 0):.2f} / "
            f"{w.get('field', 0):.2f} / {w.get('semantic', 0):.2f} / {w.get('llm', 0):.2f}"
        )

    @admin.action(description="Chọn làm bộ trọng số đang dùng")
    def activate_weight_set(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Vui lòng chọn đúng 1 bộ trọng số để kích hoạt.", level=messages.WARNING)
            return
        ws = queryset.first()
        WeightSet.objects.filter(is_active=True).update(is_active=False)
        ws.is_active = True
        ws.save()
        self.message_user(request, f"Đã kích hoạt bộ trọng số '{ws.name}'.", level=messages.SUCCESS)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "rank",
        "topic",
        "final_score",
        "m1_skill",
        "m2_academic",
        "m3_field",
        "m4_semantic",
        "m5_llm",
    )
    list_filter = ("weights_version",)


admin.site.register(LLMScore)
