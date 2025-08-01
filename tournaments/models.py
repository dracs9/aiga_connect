from decimal import Decimal

from django.conf import settings
from django.db import models

from gyms.models import Gym


class Tournament(models.Model):
    """Модель турнира"""

    LEVEL_CHOICES = [
        ("beginner", "Начинающий"),
        ("intermediate", "Средний"),
        ("advanced", "Продвинутый"),
        ("all", "Все уровни"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название турнира")
    description = models.TextField(verbose_name="Описание")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, verbose_name="Академия")
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["coach", "admin"]},
        verbose_name="Организатор",
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="all", verbose_name="Уровень"
    )
    max_participants = models.PositiveIntegerField(default=50, verbose_name="Максимум участников")
    registration_deadline = models.DateTimeField(verbose_name="Дедлайн регистрации")
    tournament_date = models.DateTimeField(verbose_name="Дата турнира")
    entry_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Взнос за участие"
    )
    prize_pool = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Призовой фонд"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"
        ordering = ["-tournament_date"]

    def __str__(self):
        return f"{self.title} - {self.gym.name}"

    @property
    def current_participants(self):
        return self.applications.filter(status="approved").count()  # type: ignore

    @property
    def is_full(self):
        return self.current_participants >= self.max_participants


class TournamentApplication(models.Model):
    """Модель заявки на турнир"""

    STATUS_CHOICES = [
        ("pending", "Ожидает рассмотрения"),
        ("approved", "Одобрена"),
        ("rejected", "Отклонена"),
        ("cancelled", "Отменена"),
    ]

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="applications", verbose_name="Турнир"
    )
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        verbose_name="Участник",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    weight_category = models.CharField(max_length=50, blank=True, verbose_name="Весовая категория")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Опыт в годах")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role__in": ["coach", "admin"]},
        related_name="processed_tournament_applications",
        verbose_name="Обработал",
    )

    class Meta:
        verbose_name = "Заявка на турнир"
        verbose_name_plural = "Заявки на турниры"
        ordering = ["-applied_at"]
        unique_together = ["tournament", "participant"]

    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.tournament.title}"
