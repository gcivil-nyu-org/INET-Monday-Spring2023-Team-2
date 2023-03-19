import datetime

from django.test import TestCase

from opportunityboard.models import Opportunity
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OpportunityTest(TestCase):
    """Test cases for Opportunity model"""

    def setUp(self):
        """See base class."""
        self.jedi = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )

    def test_opportunity_details(self):
        """Test basic opportunity details"""

        description = (
            "Please help us support our community at this week's" "Cloud City soup kitchen"
        )
        two_hours = datetime.timedelta(days=0, hours=2)
        a_date = datetime.datetime(
            year=2023,
            month=3,
            day=9,
            hour=18,
            minute=0,
        )

        soup = Opportunity.objects.create(
            organization=self.jedi,
            category="community",
            title="Cloud City Soup Kitchen",
            description=description,
            date=a_date,
            end=two_hours,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_published=False,
        )

        self.assertEqual(soup.organization.name, "Jedi Council")
        self.assertEqual(soup.category, "community")
        self.assertEqual(soup.title, "Cloud City Soup Kitchen")
        self.assertEqual(soup.description, description)
        self.assertEqual(soup.date, a_date)
        self.assertEqual(soup.end, two_hours)
        self.assertEqual(soup.address_1, "200 Calrissian Av.")
        self.assertEqual(soup.address_2, "NY")
        self.assertEqual(soup.longitude, 12.34)
        self.assertEqual(soup.latitude, 56.78)
        self.assertEqual(soup.staffing, 9)
        self.assertFalse(soup.is_published)
