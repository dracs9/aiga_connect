from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Gym


@login_required
def gym_list(request):
    """Список всех академий"""
    gyms = Gym.objects.filter(is_active=True)
    return render(request, "gyms/list.html", {"gyms": gyms})


@login_required
def gym_detail(request, pk):
    """Детальная информация об академии"""
    gym = get_object_or_404(Gym, pk=pk, is_active=True)
    return render(request, "gyms/detail.html", {"gym": gym})
