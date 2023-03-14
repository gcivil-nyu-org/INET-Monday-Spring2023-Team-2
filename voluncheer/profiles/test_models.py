from django.test import TestCase

from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer


class UserTest(TestCase):
    """Test cases for the basic user type."""

    def setUp(self):
        """See base class."""
        self.luke = Volunteer.objects.create(
            user=User.objects.create(
                email="luke@jedi.com",
                password="NOOOOOOOOOOOOOOOOOOO",
                type=UserType.VOLUNTEER,
            ),
            first_name="Luke",
            last_name="Skywalker",
            date_of_birth="1955-09-25",
            description="I want to come with you to Alderaan.",
        )
        self.jedi = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )
        self.vader = Volunteer.objects.create(
            user=User.objects.create(
                email="darth_vader@sith.com",
                password="i_am_your_father",
                type=UserType.VOLUNTEER,
            ),
            first_name="Darth",
            last_name="Vader",
            date_of_birth="1931-01-17",
        )
        self.sith = Organization.objects.create(
            user=User.objects.create(
                email="sith@sith.com",
                password="come_to_the_dark_side",
                type=UserType.ORGANIZATION,
            ),
            name="Sith Lords",
        )

        self.admin = User.objects.create_superuser(
            email="admin@starwars.com", password="admin"
        )

    def test_user_details(self):
        """Tests basic user details like active and type."""
        self.assertTrue(self.luke.user.is_active)
        self.assertTrue(self.jedi.user.is_active)
        self.assertTrue(self.vader.user.is_active)
        self.assertTrue(self.sith.user.is_active)

        self.assertTrue(self.luke.user.is_volunteer)
        self.assertTrue(self.jedi.user.is_organization)
        self.assertTrue(self.vader.user.is_volunteer)
        self.assertTrue(self.sith.user.is_organization)

    def test_organization_details(self):
        """Tests basic organization details."""
        self.assertEqual(self.jedi.name, "Jedi Council")
        self.assertEqual(self.sith.name, "Sith Lords")

    def test_volunteer_details(self):
        """Tests basic volunteer details."""
        self.assertEqual(self.luke.name, "Luke Skywalker")
        self.assertEqual(self.luke.date_of_birth, "1955-09-25")
        self.assertEqual(self.vader.name, "Darth Vader")
        self.assertEqual(self.vader.date_of_birth, "1931-01-17")
        self.assertEqual(self.luke.description, "I want to come with you to Alderaan.")

    def test_admin_details(self):
        """Tests admin account has proper attributes."""
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertEqual(self.admin.type, UserType.ADMIN)

    def test_email_is_required(self):
        """Tests creating a user without an email raises desired ValueError"""
        with self.assertRaises(ValueError):
            self.user = User.objects.create_user(email=None, password="12345")

    def test_email_max_length(self):
        """Tests email max length is 254"""
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("email").max_length
        self.assertEqual(max_length, 254)

    def test_user_object_name_is_email(self):
        """Tests User __str__ method returns email address"""
        user = User.objects.get(id=1)
        expected_object_name = f"{user.email}"
        self.assertEqual(str(user), expected_object_name)

    def test_volunteer_object_name_is_name(self):
        """Tests Volunteer __str__ method returns email address"""
        user = self.luke
        expected_object_name = f"{user.name}"
        self.assertEqual(str(user), expected_object_name)

    def test_organization_object_name_is_name(self):
        """Tests Organization __str__ method returns email address"""
        user = self.sith
        expected_object_name = f"{user.name}"
        self.assertEqual(str(user), expected_object_name)
