# from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import CreateView
from profiles.forms.volunteers import VolunteerCreationForm
from profiles.models import User, Volunteer
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

    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        volunteer_profile = Volunteer.objects.create(
            user=user,
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            date_of_birth=form.cleaned_data.get("date_of_birth"),
        )
        volunteer_profile.save()
        user.is_active = False
        user.save()
        activateEmail(self.request, user, form.cleaned_data.get("email"))
        return redirect("login")
