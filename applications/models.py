from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Application(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "WISHLIST", "Wishlist"
        APPLIED = "APPLIED", "Applied"
        INTERVIEWING = "INTERVIEWING", "Interviewing"
        OFFER = "OFFER", "Offer"
        REJECTED = "REJECTED", "Rejected"


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )


    company = models.CharField(max_length=120)
    role_title = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    job_url = models.URLField(blank=True)
    job_description = models.TextField(blank=True)


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED
    )


    date_applied = models.DateField(default=timezone.localdate)
    follow_up_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-date_applied", "-created_at"]

    def __str__(self):
        return f"{self.company} - {self.role_title}"


class ApplicationAnalysis(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="analyses"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    job_title_guess = models.CharField(max_length=200, blank=True)
    seniority_level = models.CharField(max_length=100, blank=True)
    match_score = models.PositiveIntegerField(default=0)

    fit_assessment = models.TextField(blank=True)

    required_skills = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    resume_strengths = models.JSONField(default=list, blank=True)
    missing_or_weak_skills = models.JSONField(default=list, blank=True)
    tailored_resume_suggestions = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Analysis for {self.application.company} - {self.application.role_title}"