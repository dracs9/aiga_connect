from django.urls import path

from . import views

app_name = "trainings"

urlpatterns = [
    path("", views.training_list, name="list"),
    path("<int:pk>/", views.training_detail, name="detail"),
    path("<int:pk>/apply/", views.training_apply, name="apply"),
    path("my/", views.my_trainings, name="my_trainings"),
    path("applications/", views.application_list, name="applications"),
]
