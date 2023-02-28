from django.urls import include
from django.urls import path

from profiles.views.home import home
from profiles.views.profile import ProfileView

urlpatterns = [
    path("", home, name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("organizations/", include(([
        # Here we can place organization only URLs.
    ], "profiles"), namespace="organizations")),
    path("volunteers/", include(([
        # Here we can place volunteer only URLs.
    ], "profiles"), namespace="volunteers")),
]