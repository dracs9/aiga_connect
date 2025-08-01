from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Announcement


def announcement_list(request):
    """Список объявлений"""
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'news.html', {'announcements': announcements})


def announcement_detail(request, pk):
    """Детальная информация об объявлении"""
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'news.html', {'announcement': announcement})


@login_required
def announcement_create(request):
    """Создание нового объявления"""
    if request.method == 'POST':
        # Логика создания объявления
        messages.success(request, 'Объявление успешно создано')
        return redirect('announcements:list')
    
    return render(request, 'news.html', {'create': True}) 