from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.organizations import OrganizationCreationForm
from profiles.models import User
from profiles.views.activate_email import activateEmail


class OrganizationSignUpView(CreateView):
    """Displays a form for organizations to sign up with."""

    model = User
    form_class = OrganizationCreationForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Organization"
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
