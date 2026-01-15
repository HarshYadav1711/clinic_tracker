from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.followup_create),
    path("<int:pk>/edit/", views.followup_edit),
    path("<int:pk>/done/", views.mark_done),
    path("p/<str:token>/", views.public_view),
]