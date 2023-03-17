from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView

from profiles.forms.organizations import OrganizationChangeForm
from profiles.forms.volunteers import VolunteerChangeForm
from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer
from voluncheer.settings import AWS_SES_DOMAIN
from voluncheer.settings import AWS_SES_FROM_EMAIL


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
            organization_profile = Organization.objects.get(pk=user)
            kwargs["organization"] = organization_profile
            kwargs["user_form"] = OrganizationChangeForm(instance=self.request.user)
            opportunity_lists = organization_profile.opportunity_set.all()
            kwargs["opportunity_lists"] = opportunity_lists
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
            kwargs["user_form"] = VolunteerChangeForm(instance=self.request.user)
        return super().get_context_data(**kwargs)

    def password_reset_request(request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data["email"]
                associated_user = User.objects.filter(Q(email=data)).first()
                if associated_user:
                    subject = "Password Reset Request"
                    message = render_to_string(
                        "template_reset_password.html",
                        {
                            "email": associated_user.email,
                            "user": associated_user,
                            "domain": AWS_SES_DOMAIN,
                            "site_name": "VolunCHEER",
                            "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                            "token": default_token_generator.make_token(associated_user),
                            "protocol": "https" if request.is_secure() else "http",
                        },
                    )
                    try:
                        send_mail(
                            subject,
                            message,
                            AWS_SES_FROM_EMAIL,
                            [associated_user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")
        password_reset_form = PasswordResetForm()
        return render(
            request=request,
            template_name="password_reset.html",
            context={"password_reset_form": password_reset_form},
        )


def profile_update(request):
    """Get profile update POST and call save function on ChangeForms."""
    if request.user.is_volunteer:
        form = VolunteerChangeForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
    elif request.user.is_organization:
        form = OrganizationChangeForm(request.POST, request.FILES, instance=request.user)
    else:
        raise ValueError("profile_update: user must either a volunteer or an organizaiton.")
    form.save()
    return redirect("profile")
