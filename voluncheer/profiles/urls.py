from django.urls import path

from profiles.views.activate_email import activate
from profiles.views.home import SignUpView
from profiles.views.home import home
from profiles.views.organizations import OrganizationSignUpView
from profiles.views.profile import ProfileView
from profiles.views.profile import profile_update
from profiles.views.profile import savedevents

urlpatterns = [
    path("", home, name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("savedevents", savedevents, name="saved_events"),
]
