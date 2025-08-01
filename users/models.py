from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с ролями"""

    ROLE_CHOICES = [
        ("student", "Ученик"),
        ("parent", "Родитель"),
        ("coach", "Тренер"),
        ("admin", "Администратор"),
    ]

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="student", verbose_name="Роль"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    points = models.PositiveIntegerField(default=0, verbose_name="Баллы")
    is_email_verified = models.BooleanField(default=False, verbose_name="Email подтвержден")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def is_parent(self):
        return self.role == "parent"

    @property
    def is_coach(self):
        return self.role == "coach"

    @property
    def is_admin(self):
        return self.role == "admin"
