from django.urls import path
from django.urls import re_path

from profiles.views.home import home
from profiles.views.home import SignUpView
from profiles.views.organizations import OrganizationSignUpView
from profiles.views.profile import ProfileView
from profiles.views.profile import profile_update
from profiles.views.volunteers import VolunteerSignUpView

urlpatterns = [
    path("", home, name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "signup/organization/",
        OrganizationSignUpView.as_view(),
        name="organization_signup",
    ),
    path(
        "signup/volunteer/",
        VolunteerSignUpView.as_view(),
        name="volunteer_signup",
    ),
]
