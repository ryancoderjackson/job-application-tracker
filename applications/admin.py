from django.contrib import admin
from .models import Application, ApplicationAnalysis, UserResume

# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "role_title",
        "status",
        "date_applied",
        "follow_up_date",
    )
    list_filter = ("status",)
    search_fields = ("company", "role_title")
    ordering = ("-date_applied",)

@admin.register(ApplicationAnalysis)
class ApplicationAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "match_score",
        "seniority_level",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("application__company", "application__role_title")
    ordering = ("-created_at",)

@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username", "user__email")