from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Gym(models.Model):
    """Модель академии/зала"""

    name = models.CharField(max_length=200, verbose_name="Название академии")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="gyms/", blank=True, null=True, verbose_name="Фото")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Рейтинг",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Академия"
        verbose_name_plural = "Академии"
        ordering = ["name"]

    def __str__(self):
        return self.name
