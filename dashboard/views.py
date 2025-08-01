from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from announcements.models import Announcement
from attendance.models import Attendance
from store.models import RewardClaim
from tournaments.models import Tournament, TournamentApplication
from trainings.models import Training, TrainingApplication
from users.models import User


@login_required
def home(request):
    """Главная страница личного кабинета"""
    user = request.user

    context = {
        "user": user,
        "announcements": Announcement.objects.filter(is_published=True)[:5],
    }

    if user.is_student:
        # Данные для ученика
        context.update(
            {
                "my_trainings": TrainingApplication.objects.filter(student=user, status="approved"),
                "my_tournaments": TournamentApplication.objects.filter(
                    participant=user, status="approved"
                ),
                "recent_attendance": Attendance.objects.filter(student=user)[:10],
                "my_rewards": RewardClaim.objects.filter(student=user)[:5],
            }
        )
    elif user.is_coach:
        # Данные для тренера
        context.update(
            {
                "my_trainings": Training.objects.filter(coach=user),
                "pending_applications": TrainingApplication.objects.filter(
                    training__coach=user, status="pending"
                ),
                "recent_attendance": Attendance.objects.filter(training__coach=user)[:10],
            }
        )
    elif user.is_admin:
        # Данные для администратора
        context.update(
            {
                "total_students": User.objects.filter(role="student").count(),
                "total_coaches": User.objects.filter(role="coach").count(),
                "pending_applications": TrainingApplication.objects.filter(
                    status="pending"
                ).count(),
                "pending_tournaments": TournamentApplication.objects.filter(
                    status="pending"
                ).count(),
            }
        )

    return render(request, "dashboard/home.html", context)


@login_required
def profile(request):
    """Страница профиля пользователя"""
    return render(request, "dashboard/profile.html", {"user": request.user})


@login_required
def leaderboard(request):
    """Таблица лидеров по баллам"""
    students = User.objects.filter(role="student").order_by("-points")[:20]
    return render(request, "dashboard/leaderboard.html", {"students": students})

@login_required
def logoutt(request):
    logout(request)
    return redirect("/")