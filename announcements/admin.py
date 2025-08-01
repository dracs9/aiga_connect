from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "priority", "is_published", "created_at")
    list_filter = ("priority", "is_published", "created_at")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-priority", "-created_at")
