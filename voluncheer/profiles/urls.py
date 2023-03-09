from django.urls import path
from django.urls import re_path

from profiles.views.home import home
from profiles.views.profile import ProfileView
from profiles.views.profile import profile_update
from profiles.views.volunteers import activate

urlpatterns = [
    path("", home, name="home"),
    path(r"^profile/$", ProfileView.as_view(), name="profile"),
    path(r"^profile/update/$", profile_update, name="profile_update"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
]
