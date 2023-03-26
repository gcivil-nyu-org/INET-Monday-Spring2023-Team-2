from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OpportunityboardTestCase(TestCase):
    """Test cases for Opportunityboard view"""

    def setUp(self):
        """Creating an opportunity for test_update_an_opportunity_page_loads"""
        self.org = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )
        self.category = Category.objects.create(name="Environment")
        self.subcategory = Subcategory.objects.create(name="Conservation", parent=self.category)
        self.subsubcategory = Subsubcategory.objects.create(
            name="Reforestation", parent=self.subcategory
        )
        description = (
            "Please help us support our community at this week's" "Cloud City soup kitchen"
        )
        end = "12:00:00"
        cls.date = timezone.now()
        cls.soup = Opportunity.objects.create(
            organization=cls.org,
            category=cls.category,
            subcategory=cls.subcategory,
            subsubcategory=cls.subsubcategory,
            title="Cloud City Soup Kitchen",
            description=description,
            date=cls.date,
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
        response = self.client.get(reverse("update_an_opportunity", args=[self.soup.pk]))
        self.assertIn(response.status_code, [200, 302])
