from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("logout/", views.logoutt, name="logout"),
]
