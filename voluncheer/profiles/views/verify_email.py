# views.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .home import SignUpView
from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer
from profiles.forms.organizations import OrganizationCreationForm
from django.views.generic import CreateView


class EmailVerificationView(CreateView):
    template_name = "accounts/email_verification.html"

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        uidb64 = kwargs.get("uidb64")
        try:
            uid = urlsafe_base64_encode(force_bytes(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_verified = True
            user.save()
            messages.success(
                request, "Your email has been verified. You can now log in."
            )
        else:
            messages.warning(
                request, "The confirmation link was invalid or has expired."
            )
        return redirect("login")


@login_required
def home(request):
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # send verification email
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = request.build_absolute_uri(
                reverse("email_verification", kwargs={"uidb64": uidb64, "token": token})
            )

            subject = "Verify your email address"
            message = f"Hi {user.username}, please click the link below to verify your email address: {verification_url}"
            from_email = "noreply@example.com"
            to_email = user.email

            send_mail(subject, message, from_email, [to_email])

            messages.success(
                request,
                "Your account has been created. Please check your email to verify your account.",
            )
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})
