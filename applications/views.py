from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application

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

    context = {
        "applications": qs,
        "status": status,
        "q": q,
        "status_choices": Application.Status.choices,
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