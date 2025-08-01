from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from trainings.models import Training
from gyms.models import Gym
from users.models import User

from .models import Attendance


@login_required
def attendance_list(request):
    """Список посещений"""
    if request.user.role=='student':
        attendances = Attendance.objects.filter(student=request.user).order_by("-date")
        trainings = []
        streak = len(attendances)
    else:
        attendances = Attendance.objects.filter(marked_by=request.user).order_by("-date")
        trainings = Training.objects.all().order_by("-created_at")
        # train = Training(title='Тренировка номер 2', gym=Gym.objects.get(id=1), coach=User.objects.get(id=10), duration=120)
        # train.save()
        streak = 0
    students = User.objects.filter(role='student')
    return render(request, "attendance/attendance.html",
                  {"attendances": attendances, 'is_coach': request.user.role == "coach", 'trainings': trainings,
                   "students": students, 'streak':streak})


@login_required
def mark_attendance(request):
    """Отметить посещение"""
    if request.method == "POST":
        training_id = request.POST.get("training")
        student_id = request.POST.get("studen")
        try:
            training = Training.objects.get(id=training_id)
            student = User.objects.get(id=student_id)
        except Training.DoesNotExist:
            messages.error(request, "Тренировка не найдена.")
            return redirect("attendance:mark")
        try:
            Attendance.objects.create(
                student=student,
                training=training,
                date=timezone.now().date(),
                is_present=True,
                marked_by=(
                    request.user
                    if hasattr(request.user, "role") and request.user.role == "coach"
                    else None
                ),
            )
        except Exception:
            pass
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
