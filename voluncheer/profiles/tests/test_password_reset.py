from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from profiles.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class PasswordResetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password",
            type="2",
        )
        self.test_user = User.objects.get(email="testuser@example.com")
        self.test_user.is_active = True
        self.test_user.save()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        self.token = default_token_generator.make_token(self.test_user)

    def test_password_reset_form_view(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_form.html")

    def test_password_reset_form(self):
        response = self.client.post(reverse("password_reset"), {"email": self.test_user.email})
        # self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["testuser@example.com"])
        self.assertIn("Password reset on testserver", mail.outbox[0].subject)
        self.assertIn(
            "We received a request to reset the password for your account for this email address.",
            mail.outbox[0].body,
        )
        self.assertIn(
            reverse("password_reset_confirm", args=[self.uidb64, self.token]),
            mail.outbox[0].body,
        )

    def test_password_reset_link(self):
        response = self.client.post(reverse("password_reset"), {"email": self.test_user.email})
        response = self.client.get(
            reverse("password_reset_confirm", args=[self.uidb64, self.token])
        )  # noqa E501S
        self.assertEqual(response.status_code, 302)
        # extract the URL to which the user was redirected
        redirect_url = response.url
        # make a GET request to the redirect URL
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_confirm.html")

    def test_password_reset_confirm_view(self):
        response = self.client.post(reverse("password_reset"), {"email": self.test_user.email})
        response = self.client.get(
            reverse("password_reset_confirm", args=[self.uidb64, self.token])
        )  # noqa E501S
        self.assertEqual(response.status_code, 302)
        # extract the URL to which the user was redirected
        redirect_url = response.url
        # make a GET request to the redirect URL
        response = self.client.post(
            redirect_url,
            {
                "new_password1": "new_test_password",
                "new_password2": "new_test_password",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("password_reset_complete"))

        # check that password is updated in db
        updated_user = User.objects.get(email="testuser@example.com")
        self.assertEqual(updated_user.check_password("new_test_password"), True)

    def test_password_reset_complete_view(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_complete.html")
