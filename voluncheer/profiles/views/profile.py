from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.shortcuts import redirect

from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer

from profiles.forms.volunteers import VolunteerChangeForm
from profiles.forms.organizations import OrganizationChangeForm


@method_decorator([login_required], name="dispatch")
class ProfileView(DetailView):
    """Displays a user's profile and additional type specific information."""

    model = User
    context_object_name = "user"
    template_name = "profiles/profile.html"

    def get_object(self, *args, **kwargs):
        """Returns the user object for display."""
        del args, kwargs  # Unused.
        return self.request.user

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        user = self.request.user
        if user.is_organization:
            kwargs["organization"] = Organization.objects.get(pk=user)
            kwargs["user_form"] = OrganizationChangeForm(
                instance=self.request.user
            )  # noqa: E501
        if user.is_volunteer:
            kwargs["volunteer"] = Volunteer.objects.get(pk=user)
            badge_urls = []
            badge_list = kwargs["volunteer"].badges.split(",")
            for badge in badge_list:
                try:
                    badge_urls.append(Volunteer.BADGES[badge])
                except KeyError:
                    pass
            kwargs["badge_urls"] = badge_urls
            kwargs["user_form"] = VolunteerChangeForm(
                instance=self.request.user
            )  # noqa: E501
        return super().get_context_data(**kwargs)


def profile_update(request):
    """Get profile update POST and call save function on ChangeForms."""
    if request.user.is_volunteer:
        form = VolunteerChangeForm(request.POST, instance=request.user)
    elif request.user.is_organization:
        form = OrganizationChangeForm(request.POST, instance=request.user)
    else:
        raise ValueError(
            "profile_update: user must either a volunteer or an organizaiton."
        )
    form.save()
    return redirect("profile")
