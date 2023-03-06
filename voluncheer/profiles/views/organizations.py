from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.organizations import OrganizationCreationForm
from profiles.models import User


class OrganizationSignUpView(CreateView):
    """Displays a form for organizations to sign up with."""

    model = User
    form_class = OrganizationCreationForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Organization"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save()
        login(self.request, user)
        return redirect("profile")
