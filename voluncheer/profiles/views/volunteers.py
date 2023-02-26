from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DetailView

from profiles.decorators import volunteer_required
from profiles.forms.volunteers import VolunteerCreationForm
from profiles.models import User
from profiles.models import Volunteer


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
