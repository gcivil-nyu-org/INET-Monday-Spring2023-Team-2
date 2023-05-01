import datetime

from django import test
from django.contrib.auth import get_user_model

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Badge
from profiles.models import BadgeType
from profiles.models import Organization
from profiles.models import UserType
from profiles.models import Volunteer


class TestCase(test.TestCase):
    """
    Basic set up for opportunity board tests, for use in setUp().
    Creates one of each of the following [format is Object (object_name)]:
    Start datetime (date)
    End date (end_date)
    End time (end)
    Organization (org)
    Category (category)
    Subcategory (subcategory)
    Subsubcategory (subsubcategory)
    Opportunity (opp)
    Volunteer (vol)
    """

    def setUp(self):
        super().setUp()
        self.org = Organization.objects.create(
            user=get_user_model().objects.create_user(
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
        description = "Please help us support our community at this week's soup kitchen"
        self.end = datetime.time(1, 30, 0)
        self.date = datetime.datetime(year=2023, month=5, day=8, tzinfo=datetime.timezone.utc)
        delta = datetime.timedelta(days=30)
        self.end_date = self.date + delta
        self.opp = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Cloud City Soup Kitchen",
            description=description,
            date=self.date,
            end=self.end,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=-73.966413,
            latitude=40.786174,
            staffing=9,
            is_published=True,
            is_recurring=True,
            recurrence="weekly",
            end_date=self.end_date,
        )

        self.vol = Volunteer.objects.create(
            user=get_user_model().objects.create_user(
                email="luke@jedi.com",
                password="NOOOOOOOOOOOOOOOOOOO",
                type=UserType.VOLUNTEER,
            ),
            first_name="Luke",
            last_name="Skywalker",
            date_of_birth="1955-09-25",
            description="I want to come with you to Alderaan.",
        )
        self.vol.save()

        self.gold_badge = Badge.objects.create(
            name="Gold",
            type=BadgeType.VOLUNTEER_HOURS_BADGE,
            hours_required=datetime.timedelta(hours=100),
            img="gold_badge.png",
        )
        self.silver_badge = Badge.objects.create(
            name="Silver",
            type=BadgeType.VOLUNTEER_HOURS_BADGE,
            hours_required=datetime.timedelta(hours=50),
            img="silver_badge.jpg",
        )
