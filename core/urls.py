from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .consumer import NotificationConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("documents.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]