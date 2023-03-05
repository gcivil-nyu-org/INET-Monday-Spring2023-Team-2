from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.volunteers import VolunteerCreationForm
from profiles.models import User


class VolunteerSignUpView(CreateView):
    """Displays a form for volunteers to sign up with."""

    model = User
    form_class = VolunteerCreationForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Volunteer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save()
        login(self.request, user)
        return redirect("profile")
