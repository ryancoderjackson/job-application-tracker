from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import ApplicationForm, ResumeAnalysisForm
from .models import Application, ApplicationAnalysis
from .services import analyze_resume_vs_job

# Create your views here.

@login_required
def application_list(request):
    qs = Application.objects.filter(user=request.user)

    status = request.GET.get("status", "")
    q = request.GET.get("q", "")

    if status:
        qs = qs.filter(status=status)

    if q:
        qs = qs.filter(company__icontains=q) | qs.filter(role_title__icontains=q)

    qs = qs.order_by("-date_applied")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    status_counts = (
        Application.objects
        .filter(user=request.user)
        .values("status")
        .annotate(count=Count("id"))
    )

    status_count_map = {item["status"]: item["count"] for item in status_counts}
    status_count_list = [
        (value, label, status_count_map.get(value, 0))
        for value, label in Application.Status.choices
    ]

    context = {
        "applications": page_obj,
        "status": status,
        "q": q,
        "status_choices": Application.Status.choices,
        "page_obj": page_obj,
        "status_count_list": status_count_list,
    }
    return render(request, "applications/app_list.html", context)


@login_required
def application_create(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "Application added.")
            return redirect("applications:list")
    else:
        form = ApplicationForm()

    return render(request, "applications/app_form.html", {"form": form, "mode": "create"})


@login_required
def application_update(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated.")
            return redirect("applications:list")
    else:
        form = ApplicationForm(instance=app)

    return render(request, "applications/app_form.html", {"form": form, "mode": "update", "app": app})


@login_required
def application_delete(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == "POST":
        app.delete()
        messages.success(request, "Application deleted.")
        return redirect("applications:list")

    return render(request, "applications/app_confirm_delete.html", {"app": app})

@login_required
def application_detail(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    latest_analysis = app.analyses.order_by("-created_at").first()

    context = {
        "app": app,
        "latest_analysis": latest_analysis,
    }
    return render(request, "applications/app_detail.html", context)

@login_required
def analyze_application(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    latest_analysis = app.analyses.order_by("-created_at").first()

    if request.method == "POST":
        form = ResumeAnalysisForm(request.POST)

        if not app.job_description.strip():
            messages.error(request, "This application does not have a saved job description yet.")
            return redirect("applications:analyze_application", pk=app.pk)

        if form.is_valid():
            resume_text = form.cleaned_data["resume_text"]

            try:
                result = analyze_resume_vs_job(
                    resume_text=resume_text,
                    job_description=app.job_description,
                )

                latest_analysis = ApplicationAnalysis.objects.create(
                    application=app,
                    job_title_guess=result.get("job_title_guess", ""),
                    seniority_level=result.get("seniority_level", ""),
                    match_score=result.get("match_score", 0),
                    fit_assessment=result.get("fit_assessment", ""),
                    required_skills=result.get("required_skills", []),
                    preferred_skills=result.get("preferred_skills", []),
                    resume_strengths=result.get("resume_strengths", []),
                    missing_or_weak_skills=result.get("missing_or_weak_skills", []),
                    tailored_resume_suggestions=result.get("tailored_resume_suggestions", []),
                )

                messages.success(request, "AI analysis completed successfully.")
                return redirect("applications:analyze_application", pk=app.pk)

            except Exception as error:
                messages.error(request, f"Analysis failed: {error}")

    else:
        form = ResumeAnalysisForm()

    context = {
        "app": app,
        "form": form,
        "latest_analysis": latest_analysis,
    }
    return render(request, "applications/analyze_application.html", context)