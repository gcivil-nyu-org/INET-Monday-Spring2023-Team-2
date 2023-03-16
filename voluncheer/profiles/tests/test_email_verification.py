from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, Client
from profiles.forms.organizations import OrganizationCreationForm
from profiles.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class activateEmailTest(TestCase):
    """Test cases for Email Verification"""

    def setUp(self):
        """Setting up"""
        self.client = Client()
        self.data1 = {
            "name": "Test Org",
            "email": "test_org@testing.org",
            "password1": "I_love_testing",
            "password2": "I_love_testing",
            "type": "UserType.ORGANIZATION,",
        }
        self.form1 = OrganizationCreationForm(data=self.data1)

    def test_user_inactive(self):
        """Assert User is inactive after sign up"""
        self.response = self.client.post(
            reverse("organization_signup"), data=self.form1.data
        )  # noqa E501
        test_user = User.objects.get(email="test_org@testing.org")
        self.assertFalse(test_user.is_active)

    def test_email_sent(self):
        self.response = self.client.post(
            reverse("organization_signup"), data=self.form1.data
        )  # noqa E501
        test_user = User.objects.get(email="test_org@testing.org")
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test_org@testing.org"])
        self.assertIn("Account Activation", mail.outbox[0].subject)
        self.assertIn(
            "Kindly click below given link to confirm your registration, ",
            mail.outbox[0].body,
        )
        self.assertIn(
            reverse("activate", args=[uidb64, token]),
            mail.outbox[0].body,
        )
