from django.contrib import admin

from .models import Training, TrainingApplication


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "gym", "coach", "level", "max_participants", "is_active")
    list_filter = ("level", "is_active", "gym")
    search_fields = ("title", "description", "gym__name", "coach__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "training", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("student__username", "training__title")
    readonly_fields = ("applied_at", "processed_at")
    ordering = ("-applied_at",)
