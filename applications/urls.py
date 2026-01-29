from django.urls import path
from . import views
from .views_auth import signup

app_name = "applications"

urlpatterns = [
    path("", views.application_list, name="list"),
    path("new/", views.application_create, name="create"),
    path("<int:pk>/edit/", views.application_update, name="update"),
    path("<int:pk>/delete/", views.application_delete, name="delete"),
    path("signup/", signup, name="signup"),
]
