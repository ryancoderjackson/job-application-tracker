from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company",
            "role_title",
            "location",
            "job_url",
            "status",
            "date_applied",
            "follow_up_date",
            "notes",
        ]
        widgets = {
            "company": forms.TextInput(attrs={"placeholder": "e.g., Google"}),
            "role_title": forms.TextInput(attrs={"placeholder": "e.g., Junior Software Developer"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g., Remote / Oklahoma City"}),
            "job_url": forms.URLInput(attrs={"placeholder": "Paste the job link (optional)"}),
            "date_applied": forms.DateInput(attrs={"type": "date"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 5, "placeholder": "Notes, contacts, interview details..."}),
        }
