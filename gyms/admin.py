from django.contrib import admin

from .models import Gym


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "rating", "is_active")
    list_filter = ("is_active", "rating")
    search_fields = ("name", "address", "phone", "email")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
