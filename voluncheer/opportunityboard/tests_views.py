import datetime
from django.test import TestCase
from django.urls import reverse

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OpportunityboardTestCase(TestCase):
    """Test cases for Opportunityboard view"""

    @classmethod
    def setUpTestData(cls):
        """See base class."""
        cls.jedi = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )

        cls.environment = Category.objects.create(name="Environment")

        cls.conservation = Subcategory.objects.create(name="Conservation", parent=cls.environment)

        cls.reforestation = Subsubcategory.objects.create(
            name="Reforestation", parent=cls.conservation
        )

        description = (
            "Please help us support our community at this week's" "Cloud City soup kitchen"
        )
        end = "12:00:00"
        a_date = datetime.datetime(
            year=2023,
            month=3,
            day=9,
            hour=18,
            minute=0,
        )

        cls.soup = Opportunity.objects.create(
            organization=cls.jedi,
            category=cls.environment,
            subcategory=cls.conservation,
            subsubcategory=cls.reforestation,
            title="Cloud City Soup Kitchen",
            description=description,
            date=a_date,
            end=end,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_published=False,
        )

    def test_opportunityboard_page_loads(self):
        """Tests opportunityboard page loads"""
        response = self.client.get(reverse("opportunityboard"))
        self.assertEqual(response.status_code, 200)

    def test_select_page_loads(self):
        """Tests select page loads"""
        response = self.client.get(reverse("select"))
        self.assertEqual(response.status_code, 200)

    def test_post_an_opportunity_page_loads(self):
        """Tests post_an_opportunity page loads"""
        response = self.client.get(reverse("post_an_opportunity"))
        self.assertIn(response.status_code, [200, 302])

    def test_update_an_opportunity_page_loads(self):
        """Tests update_an_opportunity page loads"""
        response = self.client.get(reverse("update_an_opportunity", args=[1]))
        self.assertIn(response.status_code, [200, 302])
