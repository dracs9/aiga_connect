from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm
from .models import User


class CustomLoginView(LoginView):
    """Кастомное представление входа"""

    form_class = CustomAuthenticationForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("dashboard:home")


class CustomLogoutView(LogoutView):
    """Кастомное представление выхода"""

    next_page = reverse_lazy("dashboard:home")


class SignUpView(CreateView):
    """Представление регистрации"""

    form_class = CustomUserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматический вход после регистрации
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, "Регистрация прошла успешно!")
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление редактирования профиля"""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("dashboard:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлен успешно!")
        return super().form_valid(form)


@login_required
def profile_view(request):
    """Представление профиля пользователя"""
    return render(request, "users/profile.html", {"user": request.user})


def role_required(role):
    """Декоратор для проверки роли пользователя"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("users:login")
            if request.user.role != role:
                messages.error(request, "У вас нет доступа к этой странице.")
                return redirect("dashboard:home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
