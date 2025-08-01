from django.contrib import admin

from .models import Reward, RewardClaim


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "points_cost", "stock", "is_active")
    list_filter = ("is_active", "points_cost")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("points_cost", "name")


@admin.register(RewardClaim)
class RewardClaimAdmin(admin.ModelAdmin):
    list_display = ("student", "reward", "status", "points_spent", "claimed_at")
    list_filter = ("status", "claimed_at")
    search_fields = ("student__username", "reward__name")
    readonly_fields = ("claimed_at", "processed_at")
    ordering = ("-claimed_at",)
