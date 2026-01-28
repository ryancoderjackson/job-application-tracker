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