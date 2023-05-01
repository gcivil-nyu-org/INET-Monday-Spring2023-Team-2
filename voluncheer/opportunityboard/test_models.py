import datetime as dt

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.unittest_setup import TestCase


class OpportunityTest(TestCase):
    """Test cases for Opportunity model"""

    def test_opportunity_details(self):
        """Test basic opportunity details"""
        self.assertEqual(self.opp.organization.name, "Jedi Council")
        self.assertEqual(self.opp.category.name, "Environment")
        self.assertEqual(self.opp.subcategory.name, "Conservation")
        self.assertEqual(self.opp.subsubcategory.name, "Reforestation")
        self.assertEqual(self.opp.title, "Cloud City Soup Kitchen")
        self.assertEqual(
            self.opp.description,
            "Please help us support our community at this week's soup kitchen",
        )
        self.assertEqual(self.opp.date, self.date)
        self.assertEqual(self.opp.end, self.end)
        self.assertEqual(self.opp.address_1, "200 Calrissian Av.")
        self.assertEqual(self.opp.address_2, "NY")
        self.assertEqual(self.opp.longitude, -73.966413)
        self.assertEqual(self.opp.latitude, 40.786174)
        self.assertEqual(self.opp.staffing, 9)
        self.assertTrue(self.opp.is_published)
        self.assertTrue(self.opp.is_recurring)
        self.assertEqual(self.opp.recurrence, "weekly")
        self.assertEqual(self.opp.end_date, self.end_date)

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

    def test_duration_property(self):
        """Tests that duration method returns correct duration"""
        expected_duration = dt.timedelta(hours=1, minutes=30)
        self.assertEqual(self.opp.duration, expected_duration)
