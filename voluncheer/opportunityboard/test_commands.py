import datetime as dt
from io import StringIO
from datetime import datetime
from datetime import timedelta
import pytz

from django.core.management import call_command
from django.test import TestCase
import freezegun

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType

_TEST_DATA = "opportunityboard/testdata/categories.json"

_CATEGORY = "Test Category"
_SUB_CATEGORY = "Test Sub Category"
_SUB_SUB_CATEGORY = "Test Sub Sub Category"


class TestLoadCategories(TestCase):
    """Tests the load categories command."""

    def test_load_categories(self):
        out = StringIO()
        call_command("load_categories", category_data=_TEST_DATA, stdout=out)
        self.assertTrue(Category.objects.filter(name=_CATEGORY).exists())
        self.assertTrue(Subcategory.objects.filter(name=_SUB_CATEGORY).exists())
        self.assertTrue(Subsubcategory.objects.filter(name=_SUB_SUB_CATEGORY).exists())

        self.assertIn("Successfully created 'Test Category'.", out.getvalue())
        self.assertIn("Successfully created 'Test Sub Category'.", out.getvalue())
        self.assertIn("Successfully created 'Test Sub Sub Category'.", out.getvalue())

        with self.subTest("test_already_exist_does_not_create_new_categories"):
            exists_out = StringIO()
            call_command("load_categories", category_data=_TEST_DATA, stdout=exists_out)
            self.assertNotIn("Successfully created 'Test Category'.", exists_out.getvalue())
            self.assertNotIn("Successfully created 'Test Sub Category'.", exists_out.getvalue())
            self.assertNotIn("Successfully created 'Test Sub Sub Category'.", exists_out.getvalue())

            self.assertEqual(len(Category.objects.all()), 1)
            self.assertEqual(len(Subcategory.objects.all()), 1)
            self.assertEqual(len(Subsubcategory.objects.all()), 1)


class TestArchiveOpportunities(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )

        self.today = dt.datetime(year=2023, month=4, day=16, tzinfo=dt.timezone.utc)
        description = "Please help us support our community at this week's soup kitchen"
        self.opportunity1 = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test opportunity 1",
            description=description,
            date=self.today - dt.timedelta(days=1),
            end=self.today - dt.timedelta(hours=1),
            is_archived=False,
            is_published=True,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_recurring=False,
        )

        self.opportunity2 = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test opportunity 2",
            description=description,
            date=self.today + dt.timedelta(days=1),
            end=self.today + dt.timedelta(hours=2),
            is_archived=False,
            is_published=True,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_recurring=False,
        )

        self.opportunity3 = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test opportunity 3",
            description=description,
            date=self.today - dt.timedelta(days=1),
            end=self.today + dt.timedelta(hours=1),
            is_archived=False,
            is_published=True,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_recurring=False,
        )
        self.opportunity4 = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test opportunity 4",
            description=description,
            date=self.today - dt.timedelta(days=1),
            end=self.today - dt.timedelta(hours=1),
            is_archived=False,
            is_published=False,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_recurring=False,
        )
        self.opportunity5 = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test opportunity 5",
            description=description,
            date=self.today - dt.timedelta(days=1),
            end=self.today - dt.timedelta(hours=1),
            is_archived=False,
            is_published=True,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_recurring=True,
        )

    def test_archive_opportunities(self):
        # freeze time when calling command:
        with freezegun.freeze_time(self.today):
            # Call the archive_opportunities command
            call_command("archive_opportunities")

            # Check if the opportunity is archived
            self.opportunity1.refresh_from_db()
            self.opportunity2.refresh_from_db()
            self.opportunity3.refresh_from_db()
            self.opportunity4.refresh_from_db()
            self.opportunity5.refresh_from_db()

            self.assertTrue(self.opportunity1.is_archived)
            self.assertFalse(self.opportunity2.is_archived)
            self.assertTrue(self.opportunity3.is_archived)
            self.assertFalse(self.opportunity4.is_archived)
            self.assertTrue(self.opportunity5.is_archived)
