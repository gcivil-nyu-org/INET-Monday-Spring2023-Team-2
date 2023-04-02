from django.test import TestCase

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.unittest_setup import setup_oppboard_tests


class PostAnOpportunityFormTest(TestCase):
    """Test cases for Post An Opportunity form"""

    def setUp(self):
        """See base class."""
        setup_oppboard_tests(self)
        self.form = PostAnOpportunityForm()
        self.sports = Category.objects.create(name="sports")
        self.healthcare = Category.objects.create(name="healthcare")
        self.animals = Category.objects.create(name="animals")

    def test_validation(self):
        """Test Post An Opportunity validation"""
        data = {
            "organization": self.org,
            "category": self.healthcare,
            "title": "Sith Surfing",
            "description": "Let's surfing",
            "staffing": "1",
            "date": self.date,
            "end": self.end,
            "address_1": "New York, NY",
            "address_2": "Down st",
            "is_published": False,
        }
        form = PostAnOpportunityForm(data=data)
        self.assertFalse(form.save())
        posted_opportunity = Opportunity.objects.get(title="Sith Surfing")
        self.assertEqual(posted_opportunity.title, "Sith Surfing")
        self.assertEqual(posted_opportunity.category.name, "healthcare")
        self.assertEqual(posted_opportunity.description, "Let's surfing")

    def test_update(self):
        """Test Update An Opportunity validation"""
        posted_opportunity = Opportunity.objects.get(title="Cloud City Soup Kitchen")
        self.assertEqual(posted_opportunity.title, "Cloud City Soup Kitchen")
        self.assertEqual(posted_opportunity.category.name, "Environment")
        self.assertEqual(
            posted_opportunity.description,
            "Please help us support our community at this week's soup kitchen",
        )
        data = {
            "organization": posted_opportunity.organization,
            "category": self.animals,
            "title": "Jedi Train",
            "description": "Face your destiny.",
            "staffing": "2",
            "date": self.date,
            "end": self.end,
            "address_1": "New York, NY",
            "address_2": "Mean st",
            "is_published": True,
        }
        form = PostAnOpportunityForm(data=data, instance=self.opp)
        self.assertFalse(form.save())
        posted_opportunity = Opportunity.objects.get(title="Jedi Train")
        self.assertEqual(posted_opportunity.title, "Jedi Train")
        self.assertEqual(posted_opportunity.category.name, "animals")

    def test_is_recurring_but_no_recurrence_raises_error(self):
        """
        Test if the Opportunity clean function raises an error if is_recurring is true but no
        recurrence is selected.
        """
        data = {
            "organization": self.org,
            "category": self.animals,
            "title": "Jedi Train",
            "description": "Face your destiny.",
            "staffing": "2",
            "date": self.date,
            "end": self.end,
            "address_1": "New York, NY",
            "address_2": "Mean st",
            "is_published": True,
            "is_recurring": True,
            "recurrence": None,  # Recurrence set to none despite is_recurring = True
        }

        form = PostAnOpportunityForm(data=data)
        self.assertFalse(form.is_valid())
