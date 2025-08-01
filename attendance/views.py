from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import Attendance


@login_required
def attendance_list(request):
    """Список посещений"""
    attendances = Attendance.objects.filter(student=request.user).order_by("-date")
    return render(request, "attendance.html", {"attendances": attendances})


@login_required
def mark_attendance(request):
    """Отметить посещение"""
    if request.method == "POST":
        # Логика отметки посещения
        Attendance.objects.create(
            student=request.user, date=timezone.now().date(), status="present"
        )
        messages.success(request, "Посещение отмечено")
        return redirect("attendance:list")

    return render(request, "attendance.html")


@login_required
def attendance_report(request):
    """Отчет по посещениям"""
    attendances = Attendance.objects.filter(student=request.user).order_by("-date")
    return render(request, "attendance.html", {"attendances": attendances, "report": True})
