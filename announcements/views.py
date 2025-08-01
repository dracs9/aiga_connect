from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Announcement


def announcement_list(request):
    """Список объявлений"""
    announcements = Announcement.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "news/news.html", {"announcements": announcements})


def announcement_detail(request, pk):
    """Детальная информация об объявлении"""
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, "news/news.html", {"announcement": announcement})


@login_required
def announcement_create(request):
    """Создание нового объявления"""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        priority = request.POST.get("priority", "medium")
        errors = []
        if not title:
            errors.append("Заголовок обязателен.")
        if not content:
            errors.append("Содержание обязательно.")
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(
                request,
                "news/news.html",
                {"create": True, "title": title, "content": content, "priority": priority},
            )
        Announcement.objects.create(
            title=title,
            content=content,
            priority=priority,
            author=request.user,
            is_published=True,
        )
        messages.success(request, "Объявление успешно создано")
        return redirect("announcements:list")

    return render(request, "news/news.html", {"create": True})
