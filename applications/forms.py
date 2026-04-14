from django import forms
from .models import Application, UserResume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company",
            "role_title",
            "location",
            "job_url",
            "job_description",
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
            "job_description": forms.Textarea(attrs={"rows": 8, "placeholder": "Paste the job description here..."}),
            "date_applied": forms.DateInput(attrs={"type": "date"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 5, "placeholder": "Notes, contacts, interview details..."}),
        }

class ResumeAnalysisForm(forms.Form):
    resume_text = forms.CharField(
        label="Resume Text",
        widget=forms.Textarea(
            attrs={
                "rows": 18,
                "placeholder": "Paste your resume text here..."
            }
        )
    )

class UserResumeForm(forms.ModelForm):
    class Meta:
        model = UserResume
        fields = ["resume_text"]
        widgets = {
            "resume_text": forms.Textarea(
                attrs={
                    "rows": 20,
                    "placeholder": "Paste your base resume text here..."
                }
            )
        }