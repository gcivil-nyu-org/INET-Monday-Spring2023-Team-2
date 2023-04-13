from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView

from opportunityboard.models import Opportunity
from profiles.forms.organizations import OrganizationChangeForm
from profiles.forms.volunteers import VolunteerChangeForm
from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer
from voluncheer.settings import AWS_SES_DOMAIN
from voluncheer.settings import DEFAULT_FROM_EMAIL


@method_decorator([login_required], name="dispatch")
class ProfileView(DetailView):
    """Displays a user's profile and additional type specific information."""

    # id = User.pk
    model = User
    context_object_name = "user"
    template_name = "profiles/profile.html"
    pk_url_kwarg = "user_id"

    def get_object(self, *args, **kwargs):
        """Returns the user object for display."""
        user_id = self.request.user.pk
        return get_object_or_404(User, pk=user_id)

    # def get_object(self, queryset=None):
    #     pk = self.kwargs.get('pk')
    #     return get_object_or_404(User, pk=pk)

    # user_id = self.request.user.pk
    # print("user_id", user_id)
    # obj = User.objects.get(pk=user_id)
    # return obj

    # del args, kwargs  # Unused.
    # return self.request.user
    # user_id = self.kwargs.get("user_id")
    # print("user_id", user_id)
    # obj = User.objects.get(pk=user_id)
    # return obj

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        user = self.request.user
        if user.is_organization:
            organization_profile = Organization.objects.get(pk=user)
            kwargs["organization"] = organization_profile
            kwargs["user_form"] = OrganizationChangeForm(instance=organization_profile)
            opportunity_lists = organization_profile.opportunity_set.all()
            kwargs["opportunity_lists"] = opportunity_lists
        if user.is_volunteer:
            volunteer_profile = Volunteer.objects.get(pk=user)
            kwargs["volunteer"] = volunteer_profile
            kwargs["user_form"] = VolunteerChangeForm(instance=volunteer_profile)
            kwargs["badges"] = volunteer_profile.badges.order_by("hours_required")
            kwargs["hours_required"] = volunteer_profile.award_volunteer_hours_badges()
            kwargs["hours_volunteered"] = round(
                volunteer_profile.hours_volunteered.total_seconds() / 3600, 2
            )

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
                            "domain": AWS_SES_DOMAIN if AWS_SES_DOMAIN else "127.0.0.1:8000",
                            "site_name": "VolunCHEER",
                            "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                            "token": default_token_generator.make_token(associated_user),
                            "protocol": "https" if request.is_secure() else "http",
                        },
                    )
                    try:
                        print()
                        send_mail(
                            subject,
                            message,
                            DEFAULT_FROM_EMAIL,
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


def profile_update(request, userid):
    """Get profile update POST and call save function on ChangeForms."""

    userid = request.user.pk
    userid = userid
    profile = get_object_or_404(User, pk=request.user.pk)

    if request.user.is_volunteer:
        profile = get_object_or_404(Volunteer, pk=request.user)
        form = VolunteerChangeForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
    elif request.user.is_organization:
        profile = get_object_or_404(Organization, pk=request.user)
        form = OrganizationChangeForm(request.POST, request.FILES, instance=profile)
    else:
        raise ValueError("profile_update: user must either a volunteer or an organizaiton.")
    form.save()
    return redirect("home")


# This part is for Volunteer specified features.


def saved_events(request):
    volunteer = get_object_or_404(Volunteer, pk=request.user.pk)
    opportunity_selected = volunteer.opportunity_set.all()
    return render(
        request=request,
        template_name="profiles/savedevents.html",
        context={
            "opportunity_selected": opportunity_selected,
            "volunteer": volunteer,
            "opportunity_attended": [],
        },
    )


# This part is for Organization specified features.


def confirm_attendance(request, opportunity_id):
    """Get the request contains volunteer selection,
    update opportunity's attended_volunteers attribute, and create archive object.
    checks to see if the volunteer is attended.
    If attended, trigger this function will cancel their attendance.
    """
    confirm_attendees = request.GET.getlist("volunteer-attended")
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
    for attendee_pk in confirm_attendees:
        volunteer = Volunteer.objects.get(pk=attendee_pk)
        if volunteer not in opportunity.volunteers.all():
            continue
        if volunteer in opportunity.attended_volunteers.all():
            opportunity.attended_volunteers.remove(volunteer)
            volunteer.hours_volunteered -= opportunity.duration
            volunteer.save()
        else:
            opportunity.attended_volunteers.add(volunteer)
            volunteer.hours_volunteered += opportunity.duration
            volunteer.save()

    return redirect("home")
