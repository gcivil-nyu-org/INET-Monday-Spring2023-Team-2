from datetime import timedelta

from django.test import TestCase

from profiles.models import Badge
from profiles.models import BadgeType
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
            photo="darth-vader.jpg",
        )
        self.sith = Organization.objects.create(
            user=User.objects.create(
                email="sith@sith.com",
                password="come_to_the_dark_side",
                type=UserType.ORGANIZATION,
            ),
            name="Sith Lords",
            photo="sith-lord.jpg",
        )

        self.admin = User.objects.create_superuser(email="admin@starwars.com", password="admin")

        self.gold_badge = Badge.objects.create(
            name="Gold",
            type=BadgeType.VOLUNTEER_LEVEL,
            hours_required=timedelta(hours=100),
            img="gold_badge.png",
        )
        self.silver_badge = Badge.objects.create(
            name="Silver",
            type=BadgeType.VOLUNTEER_LEVEL,
            hours_required=timedelta(hours=50),
            img="silver_badge.jpg",
        )

        self.luke.badges.add(self.gold_badge)
        self.luke.badges.add(self.silver_badge)

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
        self.assertEqual(self.sith.photo, "sith-lord.jpg")

    def test_volunteer_details(self):
        """Tests basic volunteer details."""
        self.assertEqual(self.luke.name, "Luke Skywalker")
        self.assertEqual(self.luke.date_of_birth, "1955-09-25")
        self.assertEqual(self.vader.name, "Darth Vader")
        self.assertEqual(self.vader.date_of_birth, "1931-01-17")
        self.assertEqual(self.vader.photo, "darth-vader.jpg")
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
        user = User.objects.get(pk=self.luke.pk)
        max_length = user._meta.get_field("email").max_length
        self.assertEqual(max_length, 254)

    def test_user_object_name_is_email(self):
        """Tests User __str__ method returns email address"""
        user = User.objects.get(pk=self.luke.pk)
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

    def test_volunteer_level(self):
        """Test that volunteer_level property returns highest volunteer level badge."""
        with self.subTest("has_badges"):
            level = self.luke.volunteer_level
            self.assertEqual(level, self.gold_badge)

        with self.subTest("has_no_badges"):
            self.luke.badges.remove(self.gold_badge)
            self.luke.badges.remove(self.silver_badge)
            level = self.luke.volunteer_level
            self.assertEqual(level, "Newbie")

    def test_award_volunteer_level_badges(self):
        """Test that volunteer is awarded a new badge and hours_remaining is returned."""
        new_badge = Badge.objects.create(
            name="Platinum",
            type=BadgeType.VOLUNTEER_LEVEL,
            hours_required=timedelta(hours=500),
            img="platinum_badge.png",
        )

        with self.subTest("badge_not_awarded"):
            self.luke.hours_volunteered = timedelta(hours=499)
            self.luke.save()
            hours_remaining = self.luke.award_volunteer_level_badges()
            self.assertFalse(self.luke.badges.filter(name=new_badge.name).exists())
            self.assertEqual(hours_remaining, 1)

        with self.subTest("badge_awarded"):
            self.luke.hours_volunteered = timedelta(hours=500)
            self.luke.save()
            hours_remaining = self.luke.award_volunteer_level_badges()
            self.assertTrue(self.luke.badges.filter(name="Platinum").exists())
            self.assertEqual(hours_remaining, None)


class BadgeTest(TestCase):
    """Test cases for Badge model"""

    def setUp(self):
        """See base class."""
        self.badge = Badge.objects.create(
            name="Gold",
            type=BadgeType.VOLUNTEER_LEVEL,
            hours_required=timedelta(hours=100),
            img="gold_badge.png",
        )

    def test_badge_details(self):
        """Test basic details for a badge like name or img"""
        self.assertEqual(self.badge.name, "Gold")
        self.assertEqual(self.badge.type, BadgeType.VOLUNTEER_LEVEL)
        self.assertEqual(self.badge.hours_required, timedelta(hours=100))
        self.assertEqual(self.badge.img, "gold_badge.png")

    def test_badge_object_name_is_name(self):
        """Test that Badge __str__ returns name"""
        badge = self.badge
        expected_object_name = f"{badge.name}"
        self.assertEqual(str(badge), expected_object_name)
