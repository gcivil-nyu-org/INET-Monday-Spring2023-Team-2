from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer


@method_decorator([login_required], name='dispatch')
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
        if user.is_volunteer:
            kwargs["volunteer"] = Volunteer.objects.get(pk=user)
        return super().get_context_data(**kwargs)
