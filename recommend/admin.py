from django.contrib import admin

from .models import LLMScore, Recommendation


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
