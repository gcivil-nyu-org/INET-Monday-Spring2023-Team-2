from django.test import TestCase

from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer

"""
Commented out for now until I figure out the namespace and app_name diff
class ProfilesTestCase(TestCase):
    def test_page_loads(self):
        c = Client()
        for url in urls.urlpatterns:
            appNameAndUrl = urls.app_name+":"+url.name
            response = c.get(reverse(appNameAndUrl))
            self.assertEqual(response.status_code, 200)
"""


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
        )
        self.sith = Organization.objects.create(
            user=User.objects.create(
                email="sith@sith.com",
                password="come_to_the_dark_side",
                type=UserType.ORGANIZATION,
            ),
            name="Sith Lords",
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
        self.assertEqual(self.vader.name, "Darth Vader")
