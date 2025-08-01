from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TrainingApplicationForm
from .models import Training, TrainingApplication


@login_required
def training_list(request):
    """Список всех тренировок"""
    trainings = Training.objects.filter(is_active=True)
    return render(request, "trainings/list.html", {"trainings": trainings})


@login_required
def training_detail(request, pk):
    """Детальная информация о тренировке"""
    training = get_object_or_404(Training, pk=pk, is_active=True)
    return render(request, "trainings/detail.html", {"training": training})


@login_required
def training_apply(request, pk):
    """Подача заявки на тренировку"""
    training = get_object_or_404(Training, pk=pk, is_active=True)

    if request.method == "POST":
        form = TrainingApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.training = training
            application.student = request.user
            application.save()
            messages.success(request, "Заявка подана успешно!")
            return redirect("trainings:detail", pk=pk)
    else:
        form = TrainingApplicationForm()

    return render(request, "trainings/apply.html", {"training": training, "form": form})


@login_required
def my_trainings(request):
    """Мои тренировки"""
    if request.user.is_student:
        applications = TrainingApplication.objects.filter(student=request.user)
    elif request.user.is_coach:
        trainings = Training.objects.filter(coach=request.user)
        return render(request, "trainings/my_trainings_coach.html", {"trainings": trainings})
    else:
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect("dashboard:home")

    return render(request, "trainings/my_trainings.html", {"applications": applications})


@login_required
def application_list(request):
    """Список заявок (для тренеров)"""
    if not request.user.is_coach:
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect("dashboard:home")

    applications = TrainingApplication.objects.filter(training__coach=request.user)
    return render(request, "trainings/applications.html", {"applications": applications})
