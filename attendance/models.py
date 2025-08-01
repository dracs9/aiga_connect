from django.conf import settings
from django.db import models

from trainings.models import Training


class Attendance(models.Model):
    """Модель учета посещений"""

    training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name="Тренировка")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        verbose_name="Ученик",
    )
    date = models.DateField(verbose_name="Дата")
    is_present = models.BooleanField(default=True, verbose_name="Присутствовал")
    points_earned = models.PositiveIntegerField(default=0, verbose_name="Заработано баллов")
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "coach"},
        related_name="marked_attendances",
        verbose_name="Отметил",
    )
    marked_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отметки")
    notes = models.TextField(blank=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"
        ordering = ["-date", "-marked_at"]
        unique_together = ["training", "student", "date"]

    def __str__(self):
        status = "присутствовал" if self.is_present else "отсутствовал"
        return f"{self.student.get_full_name()} - {self.training.title} ({status})"
