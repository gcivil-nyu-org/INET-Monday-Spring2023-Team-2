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
from profiles.models import Badge
from profiles.models import BadgeType
from profiles.models import GalleryPost
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
        pk = self.kwargs["pk"]
        return get_object_or_404(User, pk=pk)

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        kwargs["curr_user"] = self.request.user
        if user.is_organization:
            organization_profile = Organization.objects.get(pk=user)
            kwargs["organization"] = organization_profile
            kwargs["user_form"] = OrganizationChangeForm(instance=organization_profile)
            # opportunity_lists = organization_profile.opportunity_set.all()
            # POSTED OPPORTUNITIES
            posted_opportunity_lists = organization_profile.opportunity_set.filter(
                is_published=True, is_archived=False, is_recurring=False
            )
            recurring_posted_opportunity_lists = organization_profile.opportunity_set.filter(
                is_archived=False, is_recurring=True
            ).order_by("date")

            # RECURRING OPPORTUNITIES
            recurrences_to_show = []
            for opportunity in recurring_posted_opportunity_lists:
                if opportunity.pk in recurrences_to_show:
                    recurring_posted_opportunity_lists = recurring_posted_opportunity_lists.exclude(
                        pk=opportunity.pk
                    )
                else:
                    for sibling in opportunity.recurrence_siblings.all():
                        recurrences_to_show.append(sibling.pk)

            # SAVED OPPORTUNITIES
            saved_opportunity_lists = organization_profile.opportunity_set.filter(
                is_published=False, is_archived=False, is_recurring=False
            )
            # PAST OPPORTUNITIES
            past_opportunity_lists = organization_profile.opportunity_set.filter(
                is_published=True, is_archived=True
            )
            kwargs["posted_opportunity_lists"] = posted_opportunity_lists
            kwargs["recurring_posted_opportunity_lists"] = recurring_posted_opportunity_lists
            kwargs["saved_opportunity_lists"] = saved_opportunity_lists
            kwargs["past_opportunity_lists"] = past_opportunity_lists
        if user.is_volunteer:
            volunteer_profile = Volunteer.objects.get(pk=user)
            kwargs["volunteer"] = volunteer_profile
            kwargs["user_form"] = VolunteerChangeForm(instance=volunteer_profile)
            kwargs["badges"] = volunteer_profile.badges.order_by("hours_required")
            kwargs["hours_required"] = volunteer_profile.award_volunteer_hours_badges()
            kwargs["hours_volunteered"] = round(
                volunteer_profile.hours_volunteered.total_seconds() / 3600, 2
            )
            gallery_post = GalleryPost.objects.filter(volunteer=volunteer_profile)
            kwargs["gallery_post"] = gallery_post
            progress, hours_remaining, next_badge = badge_progression(volunteer_profile)
            kwargs["progress"] = progress
            kwargs["hours_remaining"] = hours_remaining
            kwargs["next_badge"] = next_badge

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
    opportunity_selected = volunteer.opportunity_set.filter(is_archived=False)
    past_opportunities = []
    archived = volunteer.opportunity_set.filter(is_archived=True)
    for opportunity in archived:
        if volunteer in opportunity.attended_volunteers.all():
            past_opportunities.append(opportunity)
    return render(
        request=request,
        template_name="profiles/savedevents.html",
        context={
            "opportunity_selected": opportunity_selected,
            "volunteer": volunteer,
            "opportunity_attended": past_opportunities,
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
        volunteer.hours_volunteered += opportunity.duration
        volunteer.save()
        opportunity.attended_volunteers.add(volunteer)
        opportunity.volunteers.remove(volunteer)
    opportunity.save()
    return redirect("home")


def badge_progression(volunteer):
    """Returns the progress and hours remaining to the next progression badge and the badge.

    Args:
        volunteer: the volunteer for whose progress to compute.

    Returns:
        A three item tuple containing the progress percentage (represented as an integer between 0
        and 100), the hours that remain until the next badge, and the next badge the volunteer can
        earn.
    """
    badges = Badge.objects.filter(type=BadgeType.VOLUNTEER_HOURS_BADGE).order_by("hours_required")
    volunteer_badges = volunteer.badges.order_by("hours_required")
    for i, badge in enumerate(badges):
        if badge in volunteer_badges:
            continue
        hours_required = badge.hours_required.total_seconds() / 3600
        hours_accumulated = volunteer.hours_volunteered.total_seconds() / 3600
        if i > 0:
            previous_badge_hours = badges[i - 1].hours_required.total_seconds() / 3600
            hours_required = hours_required - previous_badge_hours
            hours_accumulated = hours_accumulated - previous_badge_hours

        progress = hours_accumulated / hours_required * 100
        hours_remaining = hours_required - hours_accumulated
        return progress, hours_remaining, badge
    return 0, 0, badges[0]
