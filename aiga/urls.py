"""
URL configuration for aiga project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("users/", include("users.urls")),
    path("trainings/", include("trainings.urls")),
    path("tournaments/", include("tournaments.urls")),
    path("attendance/", include("attendance.urls")),
    path("store/", include("store.urls")),
    path("announcements/", include("announcements.urls")),
    path("gyms/", include("gyms.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
