from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "points", "is_active")
    list_filter = ("role", "is_active", "is_email_verified")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = list(UserAdmin.fieldsets) + [
        (
            "AIGA Connect",
            {"fields": ("role", "phone", "birth_date", "points", "is_email_verified")},
        ),
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        ("AIGA Connect", {"fields": ("role", "phone", "birth_date")}),
    ]
