from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.followup_create, name="followup_create"),
    path("<int:pk>/edit/", views.followup_edit, name="followup_edit"),
    path("<int:pk>/done/", views.mark_done, name="mark_done"),
    path("<int:pk>/delete/", views.followup_delete, name="followup_delete"),
    path("p/<str:token>/", views.public_view, name="public_view"),
]