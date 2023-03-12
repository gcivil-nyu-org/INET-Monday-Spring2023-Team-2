from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from profiles.forms.organizations import OrganizationCreationForm
from profiles.models import User, Organization
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages


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
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        organization_profile = Organization.objects.create(
            user=user,
            name=form.cleaned_data.get("name"),
        )
        organization_profile.save()
        user.is_active = False
        user.save()
        activateEmail(self.request, user, form.cleaned_data.get("email"))
        return redirect("login")


def activateEmail(request, user, to_email):
    subject = "Account Activation"
    message = render_to_string(
        "registration/template_activate_account.html",
        {
            "email": user.email,
            "user": user,
            "domain": "127.0.0.1:8000",
            "site_name": "VolunCHEER",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    try:
        send_mail(
            subject,
            message,
            "admin@admin.com",
            [to_email],
            fail_silently=False,  # noqa E501
        )  # noqa E501
        messages.success(
            request,
            f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
        the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.",  # noqa E501
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    return redirect("login")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token:
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",  # noqa E501
        )
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("signup")
