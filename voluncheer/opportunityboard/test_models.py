import datetime

from django.test import TestCase

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OpportunityTest(TestCase):
    """Test cases for Opportunity model"""

    @classmethod
    def setUpTestData(cls):
        """See base class."""
        cls.org = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )

        cls.category = Category.objects.create(name="Environment")

        cls.subcategory = Subcategory.objects.create(name="Conservation", parent=cls.category)

        cls.subsubcategory = Subsubcategory.objects.create(
            name="Reforestation", parent=cls.subcategory
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
            organization=cls.org,
            category=cls.category,
            subcategory=cls.subcategory,
            subsubcategory=cls.subsubcategory,
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

    def test_opportunity_details(self):
        """Test basic opportunity details"""
        self.assertEqual(self.soup.organization.name, "Jedi Council")
        self.assertEqual(self.soup.category.name, "Environment")
        self.assertEqual(self.soup.subcategory.name, "Conservation")
        self.assertEqual(self.soup.subsubcategory.name, "Reforestation")
        self.assertEqual(self.soup.title, "Cloud City Soup Kitchen")
        self.assertEqual(
            self.soup.description,
            "Please help us support our community at this week's" "Cloud City soup kitchen",
        )
        self.assertEqual(
            self.soup.date,
            datetime.datetime(
                year=2023,
                month=3,
                day=9,
                hour=18,
                minute=0,
            ),
        )
        self.assertEqual(self.soup.end, "12:00:00")
        self.assertEqual(self.soup.address_1, "200 Calrissian Av.")
        self.assertEqual(self.soup.address_2, "NY")
        self.assertEqual(self.soup.longitude, 12.34)
        self.assertEqual(self.soup.latitude, 56.78)
        self.assertEqual(self.soup.staffing, 9)
        self.assertFalse(self.soup.is_published)

    def test_category_details(self):
        """Test basic category details"""
        category = self.category
        self.assertEqual(category.name, "Environment")

    def test_subcategory_details(self):
        """Test basic subcategory details"""
        subcategory = self.subcategory
        self.assertEqual(subcategory.name, "Conservation")
        self.assertEqual(subcategory.parent.name, "Environment")

    def test_subsubcategory_details(self):
        """Test basic subsubcategory details"""
        subsubcategory = self.subsubcategory
        self.assertEqual(subsubcategory.name, "Reforestation")
        self.assertEqual(subsubcategory.parent.name, "Conservation")

    def test_opportunity_object_name_is_title(self):
        """Tests Opportunity __str__ method returns title"""
        opportunity = Opportunity.objects.get(title="Cloud City Soup Kitchen")
        expected_opportunity_name = f"{opportunity.title}"
        self.assertEqual(str(opportunity), expected_opportunity_name)

    def test_category_object_name_is_name(self):
        """Tests Category __str__ method returns name"""
        category = Category.objects.get(name="Environment")
        expected_category_name = f"{category.name}"
        self.assertEqual(str(category), expected_category_name)

    def test_subcategory_object_name_is_full_path(self):
        """Tests Subcategory __str__ method returns name"""
        subcategory = Subcategory.objects.get(name="Conservation")
        expected_subcategory_name = f"{subcategory.name}"
        self.assertEqual(str(subcategory), expected_subcategory_name)

    def test_subsubcategory_object_name_is_full_path(self):
        """Tests Subsubcategory __str__ method returns name"""
        subsubcategory = Subsubcategory.objects.get(name="Reforestation")
        expected_subsubcategory_name = f"{subsubcategory.name}"
        self.assertEqual(str(subsubcategory), expected_subsubcategory_name)
