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
        self.assertEqual(self.user.opportunity_set.all().count(), 1)
        self.assertFalse(form.save())
        self.assertEqual(self.user.opportunity_set.all().count(), 2)
        posted_opportunity = Opportunity.objects.get(pk=2)
        self.assertEqual(posted_opportunity.title, "Sith Surfing")
        self.assertEqual(posted_opportunity.category.name, "healthcare")
        self.assertEqual(posted_opportunity.description, "Let's surfing")

    def test_update(self):
        """Test Update An Opportunity validation"""
        posted_opportunity = Opportunity.objects.get(pk=1)
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
        form = PostAnOpportunityForm(data=data)
        self.assertEqual(self.user.opportunity_set.all().count(), 1)
        self.assertFalse(form.update(1))
        posted_opportunity = Opportunity.objects.get(pk=1)
        self.assertEqual(self.user.opportunity_set.all().count(), 1)
        self.assertEqual(posted_opportunity.title, "Jedi Train")
        self.assertEqual(posted_opportunity.category.name, "animals")
