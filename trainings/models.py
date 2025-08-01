from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models

from gyms.models import Gym

if TYPE_CHECKING:
    from .models import TrainingApplication


class Training(models.Model):
    """Модель тренировки"""

    LEVEL_CHOICES = [
        ("beginner", "Начинающий"),
        ("intermediate", "Средний"),
        ("advanced", "Продвинутый"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название тренировки")
    description = models.TextField(verbose_name="Описание")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, verbose_name="Академия")
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "coach"},
        verbose_name="Тренер",
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="beginner", verbose_name="Уровень"
    )
    max_participants = models.PositiveIntegerField(default=20, verbose_name="Максимум участников")
    duration = models.PositiveIntegerField(
        help_text="Длительность в минутах", verbose_name="Длительность"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Стоимость"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.gym.name}"

    @property
    def current_participants(self):
        return self.applications.filter(status="approved").count()  # type: ignore

    @property
    def is_full(self):
        return self.current_participants >= self.max_participants


class TrainingApplication(models.Model):
    """Модель заявки на тренировку"""

    STATUS_CHOICES = [
        ("pending", "Ожидает рассмотрения"),
        ("approved", "Одобрена"),
        ("rejected", "Отклонена"),
        ("cancelled", "Отменена"),
    ]

    training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name="applications", verbose_name="Тренировка"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        verbose_name="Ученик",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    message = models.TextField(blank=True, verbose_name="Сообщение")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "coach"},
        related_name="processed_applications",
        verbose_name="Обработал",
    )

    class Meta:
        verbose_name = "Заявка на тренировку"
        verbose_name_plural = "Заявки на тренировки"
        ordering = ["-applied_at"]
        unique_together = ["training", "student"]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.training.title}"
