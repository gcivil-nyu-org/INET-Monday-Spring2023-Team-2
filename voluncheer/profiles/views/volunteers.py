from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.volunteers import VolunteerCreationForm
from profiles.models import User
from profiles.views.activate_email import activateEmail


class VolunteerSignUpView(CreateView):
    """Displays a form for volunteers to sign up with."""

    model = User
    form_class = VolunteerCreationForm
    template_name = "registration/signup_form.html"
    # volunteer_profile = {}

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Volunteer"
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save()
        user.is_active = False
        user.save()
        try:
            activateEmail(self.request, user, form.cleaned_data.get("email"))
        except Exception:
            # Delete the user if an error occurs
            print("here!")
            user.delete()

            #  Show an error message to the user
            messages.error(
                self.request,
                "We encountered an error while sending the activation email."
                "Please try again soon.",
            )

            return redirect("signup")

        return redirect("login")
