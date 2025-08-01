from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Reward, RewardClaim


def store_list(request):
    """Список наград в магазине"""
    rewards = Reward.objects.filter(is_active=True).order_by("name")
    return render(request, "store/store.html", {"rewards": rewards})


def product_detail(request, pk):
    """Детальная информация о награде"""
    reward = get_object_or_404(Reward, pk=pk)
    return render(request, "store/store.html", {"reward": reward})


@login_required
def cart_view(request):
    """Корзина пользователя"""
    # Логика корзины
    return render(request, "store/store.html", {"cart": True})


@login_required
def checkout(request):
    """Оформление заказа"""
    if request.method == "POST":
        # Логика оформления заказа
        messages.success(request, "Заказ успешно оформлен")
        return redirect("store:list")

    return render(request, "store/store.html", {"checkout": True})
