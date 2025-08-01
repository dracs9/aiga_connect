from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Reward, RewardClaim


def store_list(request):
    """Список наград в магазине и добавление новой награды (для тренеров/админов)"""
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.role in ["coach", "admin"]
    ):
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        points_cost = request.POST.get("points_cost", "").strip()
        stock = request.POST.get("stock", "").strip()
        image = request.FILES.get("image")
        errors = []
        if not name:
            errors.append("Название обязательно.")
        if not description:
            errors.append("Описание обязательно.")
        if not points_cost or not points_cost.isdigit() or int(points_cost) < 0:
            errors.append("Стоимость должна быть неотрицательным числом.")
        if not stock or not stock.isdigit() or int(stock) < 0:
            errors.append("Количество должно быть неотрицательным числом.")
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            Reward.objects.create(
                name=name,
                description=description,
                points_cost=int(points_cost),
                stock=int(stock),
                image=image,
                is_active=True,
            )
            messages.success(request, "Награда успешно добавлена!")
            return redirect("store:list")
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
    """Оформление заказа (получение награды студентом)"""
    if request.method == "POST":
        reward_id = request.POST.get("reward_id")
        reward = Reward.objects.filter(id=reward_id, is_active=True).first()
        if not reward:
            messages.error(request, "Награда не найдена или неактивна.")
            return redirect("store:list")
        if request.user.role != "student":
            messages.error(request, "Только студенты могут получать награды.")
            return redirect("store:list")
        if reward.points_cost > request.user.points:
            messages.error(request, "Недостаточно баллов для получения награды.")
            return redirect("store:list")
        if reward.stock < 1:
            messages.error(request, "Награда закончилась.")
            return redirect("store:list")
        if RewardClaim.objects.filter(
            reward=reward, student=request.user, status="pending"
        ).exists():
            messages.error(request, "У вас уже есть заявка на эту награду, ожидающая обработки.")
            return redirect("store:list")
        RewardClaim.objects.create(
            reward=reward,
            student=request.user,
            points_spent=reward.points_cost,
            status="pending",
        )
        reward.stock -= 1
        reward.save()
        request.user.points -= reward.points_cost
        request.user.save()
        messages.success(request, "Заявка на получение награды отправлена!")
        return redirect("store:list")
    return render(request, "store/store.html", {"checkout": True})
