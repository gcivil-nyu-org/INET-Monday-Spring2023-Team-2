import random
import string
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from profiles.models import User, UserType


class TestCreateSuperUser(TestCase):
    """Tests the create super user command."""

    def setUp(self):
        self.email = "super@admin.com"
        self.password = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

    def test_creates_super_user(self):
        out = StringIO()
        call_command("create_su", email=self.email, password=self.password, stdout=out)
        self.assertTrue(User.objects.filter(email=self.email).exists())

    def test_already_exists(self):
        User.objects.create_superuser(
            email=self.email,
            password=self.password,
            is_active=True,
            type=UserType.ADMIN,
        )
        out = StringIO()
        call_command("create_su", email=self.email, password=self.password, stdout=out)
        self.assertIn("already exists", out.getvalue())
