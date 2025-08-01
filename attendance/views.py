from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from trainings.models import Training

from .models import Attendance


@login_required
def attendance_list(request):
    """Список посещений"""
    attendances = Attendance.objects.filter(student=request.user).order_by("-date")
    return render(request, "attendance/attendance.html", {"attendances": attendances})


@login_required
def mark_attendance(request):
    """Отметить посещение"""
    if request.method == "POST":
        training_id = request.POST.get("training")
        try:
            training = Training.objects.get(id=training_id)
        except Training.DoesNotExist:
            messages.error(request, "Тренировка не найдена.")
            return redirect("attendance:mark")
        Attendance.objects.create(
            student=request.user,
            training=training,
            date=timezone.now().date(),
            is_present=True,
            marked_by=(
                request.user
                if hasattr(request.user, "role") and request.user.role == "coach"
                else None
            ),
        )
        messages.success(request, "Посещение отмечено")
        return redirect("attendance:list")

    # GET: показать форму выбора тренировки
    trainings = Training.objects.filter(is_active=True)
    return render(request, "attendance/attendance.html", {"trainings": trainings})


@login_required
def attendance_report(request):
    """Отчет по посещениям"""
    attendances = Attendance.objects.filter(student=request.user).order_by("-date")
    return render(
        request, "attendance/attendance.html", {"attendances": attendances, "report": True}
    )
