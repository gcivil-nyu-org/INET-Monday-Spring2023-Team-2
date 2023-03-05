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
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views

from profiles.views.home import SignUpView
from profiles.views.organizations import OrganizationSignUpView
from profiles.views.volunteers import VolunteerSignUpView, ActivateView

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("", include("profiles.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/signup/organization/", OrganizationSignUpView.as_view(),
         name="organization_signup"),
    path("accounts/signup/volunteer/", VolunteerSignUpView.as_view(),
         name="volunteer_signup"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         ActivateView.as_view(), name='activate'),
    # path("accounts/signup/volunteer/verification", VolunteerSignUpView.as_view(),
    #      name="email_verification"),
    # path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    # path('check-email/', CheckEmailView.as_view(), name="check_email"),
    # Unimplemented urls.
    # path('success/', SuccessView.as_view(), name="success"),
    # path("chat/", include("chatroom.urls")),
    # path("jobboard/", include("job_board.urls")),
    # path("map/", include("map.urls")),
]
