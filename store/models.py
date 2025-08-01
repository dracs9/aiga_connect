from django.conf import settings
from django.db import models


class Reward(models.Model):
    """Модель награды/товара в магазине"""

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    points_cost = models.PositiveIntegerField(verbose_name="Стоимость в баллах")
    image = models.ImageField(upload_to="rewards/", blank=True, null=True, verbose_name="Фото")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"
        ordering = ["points_cost", "name"]

    def __str__(self):
        return f"{self.name} ({self.points_cost} баллов)"

    @property
    def is_available(self):
        return self.is_active and self.stock > 0


class RewardClaim(models.Model):
    """Модель заявки на получение награды"""

    STATUS_CHOICES = [
        ("pending", "Ожидает обработки"),
        ("approved", "Одобрена"),
        ("rejected", "Отклонена"),
        ("completed", "Выдана"),
    ]

    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, verbose_name="Награда")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        verbose_name="Ученик",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    points_spent = models.PositiveIntegerField(verbose_name="Потрачено баллов")
    claimed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role__in": ["coach", "admin"]},
        related_name="processed_rewards",
        verbose_name="Обработал",
    )
    notes = models.TextField(blank=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Заявка на награду"
        verbose_name_plural = "Заявки на награды"
        ordering = ["-claimed_at"]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.reward.name}"
