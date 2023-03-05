from django.contrib import messages
from django.contrib.auth import login, authenticate

from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from verify_email.email_handler import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView

# from profiles.decorators import user_not_authenticated

from profiles.forms.volunteers import VolunteerCreationForm
from profiles.models import User
from profiles.tokens import account_activation_token
UserModel = get_user_model()


# def activateEmail(request, user, to_email):
#     messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#                 received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')

# class ActivateAccount(View):

#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             messages.success(request, ('Your account have been confirmed.'))
#             return redirect('home')
#         else:
#             messages.warning(
#                 request, ('The confirmation link was invalid, possibly because it has already been used.'))
#             return redirect('home')


class VolunteerSignUpView(CreateView):
    """Displays a form for volunteers to sign up with."""
    model = User
    form_class = VolunteerCreationForm
    template_name = "registration/signup_form.html"
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Volunteer"
        return super().get_context_data(**kwargs)

    def signup(request):
        if request.method == 'POST':
            form = VolunteerCreationForm(request.POST)
            if form.is_valid():
                # the form has to be saved in the memory and not in DB
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # This is  to obtain the current cite domain

                mail_subject = 'The Activation link has been sent to your email address'
                message = render_to_string('registration/activate_account.html', {
                    'user': user,
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_str(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                try:
                    send_mail(mail_subject, message, 'admin@admin.com',
                              [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("registration/check_email.html")
        else:
            form = VolunteerCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    # def signup(request):
    #     if request.method == 'POST':
    #         form = VolunteerCreationForm(request.POST)
    #         if form.is_valid():
    #             # the form has to be saved in the memory and not in DB
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
    #             # This is  to obtain the current cite domain
    #             current_site_info = get_current_site(request)
    #             mail_subject = 'The Activation link has been sent to your email address'
    #             message = render_to_string('registration/activate_account.html', {
    #                 'user': user,
    #                 'domain': current_site_info.domain,
    #                 'uid': urlsafe_base64_encode(force_str(user.pk)),
    #                 'token': account_activation_token.make_token(user),
    #             })
    #             to_email = form.cleaned_data.get('email')
    #             email = EmailMessage(
    #                 mail_subject, message, to=[to_email]
    #             )
    #             email.send()
    #             return HttpResponse('Please proceed confirm your email address to complete the registration')
    #     else:
    #         form = VolunteerCreationForm()
    #     return render(request, 'registration/signup.html', {'form': form})

    # def form_valid(self, form):
    #     to_return = super().form_valid(form)

    #     user = form.save()
    #     user.is_active = False  # Turns the user status to inactive
    #     user.save()

    #     form.send_activation_email(self.request, user)

    #     return to_return

    # def register(request):
    #     if request.method == "POST":
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             data = form.cleaned_data['email']
    #             subject = "Email Verification Request"
    #             message = render_to_string("template_reset_password.html", {
    #                 'email': user.email,
    #                 'user': user,
    #                 'domain': '127.0.0.1:8000',
    #                 'site_name': 'VolunCHEER',
    #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #                 'token': default_token_generator.make_token(user),
    #                 "protocol": 'https' if request.is_secure() else 'http'
    #             })
    #             print("works here")
    #             try:
    #                 send_mail(subject, message, 'admin@admin.com',
    #                           [user.email], fail_silently=False)
    #             except BadHeaderError:
    #                 return HttpResponse('Invalid header found.')
    #             return redirect("/password_reset/done/")
    #     password_reset_form = PasswordResetForm()
    #     print("works here tooo")
    #     return render(request=request, template_name="password_reset.html", context={"password_reset_form": password_reset_form})

    # def register(request):
    #     if request.method == "POST":
    #         form = UserCreationForm(request.POST)
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
    #             # login(request, user)
    #             activate(request, user, form.cleaned_data.get('email'))
    #             return redirect('registration')

    #         else:
    #             for error in list(form.errors.values()):
    #                 messages.error(request, error)

    #     else:
    #         form = UserCreationForm()

    #     return render(
    #         request=request,
    #         template_name="email-verification.html",
    #         context={"form": form}
    #     )

    # def activate(request, user, to_email):
    #     mail_subject = 'Activate your user account.'
    #     message = render_to_string('email_verification.html', {
    #         'user': user.username,
    #         'domain': get_current_site(request).domain,
    #         'uid': urlsafe_base64_encode(force_str(user.pk)),
    #         'token': account_activation_token.make_token(user),
    #         'protocol': 'https' if request.is_secure() else 'http'
    #     })
    #     email = EmailMessage(mail_subject, message, to=[to_email])
    #     if email.send():
    #         messages.success(
    #             request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    #     else:
    #         messages.error(
    #             request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

    # def signup(request):
        # if request.method == 'POST':
        #     form = VolunteerCreationForm(request.POST)
        #     if form.is_valid():
        #         user = form.save(commit=False)
        #         user.is_active = False
        #         user.save()
        #         current_site = get_current_site(request)
        #         mail_subject = 'Activate your Voluncheer account.'
        #         message = render_to_string('email_verification.html', {
        #             'user': user,
        #             'domain': current_site.domain,
        #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #             'token': account_activation_token.make_token(user),
        #         })
        #         to_email = form.cleaned_data.get('email')
        #         email = EmailMessage(
        #             mail_subject, message, to=[to_email]
        #         )
        #         email.send()
        #         return HttpResponse('Please confirm your email address to complete the registration')
        # else:
        #     form = VolunteerCreationForm()
        # return render(request, 'signup.html', {'form': form})

    # def activate(request, uidb64, token):
    #     try:
    #         uid = force_str(urlsafe_base64_decode(uidb64))
    #         user = User.objects.get(pk=uid)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None
    #     if user is not None and account_activation_token.check_token(user, token):
    #         user.is_active = True
    #         user.save()
    #         login(request, user)
    #         # return redirect('home')
    #         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    #     else:
    #         return HttpResponse('Activation link is invalid!')
    # def form_valid(self, form):
    #     """Saves the new user and logs them in."""
    #     # if form.is_valid():
    #     #     inactive_user = send_verification_email(self.request, form)
    #     user = form.save()
    #     user.save()
    #     login(self.request, user)
    #     return redirect("profile")
        # if self.request.method == "POST":
        #     email_verification = VolunteerCreationForm(self.request.POST)
        #     if email_verification.is_valid():
        #         user = email_verification.save(commit=False)
        #         user.is_active = False
        #         user.save()
        #         data = email_verification.cleaned_data('email')
        #         activateEmail(self.request, user, data)
        #         return redirect("profile")


class ActivateView(RedirectView):
    def activate(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
