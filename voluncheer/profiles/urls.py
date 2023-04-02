from django.urls import path

from profiles.views.activate_email import activate
from profiles.views.home import SignUpView
from profiles.views.home import home
from profiles.views.organizations import OrganizationSignUpView
from profiles.views.profile import ProfileView
from profiles.views.profile import profile_update
from profiles.views.profile import saved_events
from profiles.views.volunteers import VolunteerSignUpView

urlpatterns = [
    path("", home, name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path(
        "accounts/signup/organization/",
        OrganizationSignUpView.as_view(),
        name="organization_signup",
    ),
    path(
        "accounts/signup/volunteer/",
        VolunteerSignUpView.as_view(),
        name="volunteer_signup",
    ),
    path("savedevents/", saved_events, name="saved_events"),
]
