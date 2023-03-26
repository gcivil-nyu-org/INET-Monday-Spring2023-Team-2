from django.test import TestCase
from django.utils import timezone

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class PostAnOpportunityFormTest(TestCase):
    """Test cases for Post An Opportunity form"""

    def setUp(self):
        """See base class."""
        self.form = PostAnOpportunityForm()
        self.user = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )
        self.user.save()
        self.sports = Category.objects.create(name="sports")
        self.healthcare = Category.objects.create(name="healthcare")
        self.animals = Category.objects.create(name="animals")
        self.opportunity = Opportunity.objects.create(
            pubdate=timezone.now(),
            organization=self.user,
            category=self.sports,
            title="Jedi Trial",
            description="Face your destiny.",
            staffing="1",
            date=timezone.now(),
            end="12:00:00",
            address_1="New York, NY",
            address_2="Mean st",
            is_published=False,
            photo="sith-lord.jpg",
            is_recurring=True,
            recurrence="weekly",
        )
        self.opportunity.save()

    def test_validation(self):
        """Test Post An Opportunity validation"""
        data = {
            "organization": self.user,
            "category": self.healthcare,
            "title": "Sith Surfing",
            "description": "Let's surfing",
            "staffing": "1",
            "date": timezone.now(),
            "end": "12:00:00",
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
        posted_opportunity = Opportunity.objects.get(title="Jedi Trial")
        self.assertEqual(posted_opportunity.title, "Jedi Trial")
        self.assertEqual(posted_opportunity.category.name, "sports")
        self.assertEqual(posted_opportunity.description, "Face your destiny.")
        data = {
            "organization": posted_opportunity.organization,
            "category": self.animals,
            "title": "Jedi Train",
            "description": "Face your destiny.",
            "staffing": "2",
            "date": timezone.now(),
            "end": "12:00:00",
            "address_1": "New York, NY",
            "address_2": "Mean st",
            "is_published": True,
        }
        form = PostAnOpportunityForm(data=data, instance=posted_opportunity)
        self.assertFalse(form.save())
        posted_opportunity = Opportunity.objects.get(title="Jedi Train")
        self.assertEqual(posted_opportunity.title, "Jedi Train")
        self.assertEqual(posted_opportunity.category.name, "animals")

    def test_clean(self):
        """Test if clean function properly raises errors"""
        data = {
            "organization": self.user,
            "category": self.animals,
            "title": "Jedi Train",
            "description": "Face your destiny.",
            "staffing": "2",
            "date": timezone.now(),
            "end": "12:00:00",
            "address_1": "New York, NY",
            "address_2": "Mean st",
            "is_published": True,
            "is_recurring": True,
            "recurrence": None,  # Recurrence set to none despite is_recurring = True
        }

        form = PostAnOpportunityForm(data=data)
        self.assertFalse(form.is_valid())
