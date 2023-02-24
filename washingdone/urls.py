from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls", namespace="web")),
    path("app/", include("app.urls", namespace="app")),
    path("tinymce/", include("tinymce.urls")),
]
