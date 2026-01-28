from django.contrib import admin
from .models import Application

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