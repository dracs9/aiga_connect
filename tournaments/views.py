from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Tournament, TournamentApplication


def tournament_list(request):
    """Список всех турниров"""
    tournaments = Tournament.objects.filter(is_active=True).order_by("tournament_date")
    return render(request, "tournaments/tournament.html", {"tournaments": tournaments})


def tournament_detail(request, pk):
    """Детальная информация о турнире"""
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, "tournaments/tournament.html", {"tournament": tournament})


@login_required
def tournament_apply(request, pk):
    """Подача заявки на турнир"""
    tournament = get_object_or_404(Tournament, pk=pk)

    if request.method == "POST":
        # Проверяем, не подавал ли уже пользователь заявку
        existing_application = TournamentApplication.objects.filter(
            tournament=tournament, participant=request.user
        ).first()

        if existing_application:
            messages.error(request, "Вы уже подавали заявку на этот турнир")
        else:
            TournamentApplication.objects.create(
                tournament=tournament, participant=request.user, status="pending"
            )
            messages.success(request, "Заявка успешно подана")

        return redirect("tournaments:detail", pk=pk)

    return redirect("tournaments:detail", pk=pk)


@login_required
def my_tournaments(request):
    """Мои турниры (для участников) или организованные турниры (для организаторов)"""
    if request.user.role in ["coach", "admin"]:
        # Для организаторов показываем созданные ими турниры
        tournaments = Tournament.objects.filter(organizer=request.user)
    else:
        # Для участников показываем турниры, на которые они подали заявки
        applications = TournamentApplication.objects.filter(participant=request.user)
        tournaments = [app.tournament for app in applications]

    return render(request, "tournaments/tournament.html", {"tournaments": tournaments})
