"""voluncheer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from voluncheer import settings
from voluncheer.environment import environment

urlpatterns = [
    path("", include("profiles.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("map/", include("map.urls")),
    path("opportunityboard/", include("opportunityboard.urls")),
]

if not environment.is_aws:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    debug_path = [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns.extend(debug_path)
