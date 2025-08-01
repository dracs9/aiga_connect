from django.contrib import admin

from .models import Tournament, TournamentApplication


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("title", "gym", "organizer", "tournament_date", "is_active")
    list_filter = ("level", "is_active", "gym")
    search_fields = ("title", "description", "gym__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-tournament_date",)


@admin.register(TournamentApplication)
class TournamentApplicationAdmin(admin.ModelAdmin):
    list_display = ("participant", "tournament", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("participant__username", "tournament__title")
    readonly_fields = ("applied_at", "processed_at")
    ordering = ("-applied_at",)
