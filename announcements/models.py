from django.conf import settings
from django.db import models


class Announcement(models.Model):
    """Модель объявления"""

    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
        ("urgent", "Срочный"),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["coach", "admin"]},
        verbose_name="Автор",
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium", verbose_name="Приоритет"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-priority", "-created_at"]

    def __str__(self):
        return self.title
