from django.urls import path

from . import views

app_name = "announcements"

urlpatterns = [
    path("", views.announcement_list, name="list"),
    path("<int:pk>/", views.announcement_detail, name="detail"),
    path("create/", views.announcement_create, name="create"),
]
