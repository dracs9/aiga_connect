from django.urls import path

from . import views

app_name = "tournaments"

urlpatterns = [
    path("", views.tournament_list, name="list"),
    path("<int:pk>/", views.tournament_detail, name="detail"),
    path("<int:pk>/apply/", views.tournament_apply, name="apply"),
    path("my/", views.my_tournaments, name="my_tournaments"),
]
