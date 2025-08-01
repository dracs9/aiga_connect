from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "training", "date", "is_present", "points_earned")
    list_filter = ("is_present", "date", "training")
    search_fields = ("student__username", "training__title")
    readonly_fields = ("marked_at",)
    ordering = ("-date", "-marked_at")
