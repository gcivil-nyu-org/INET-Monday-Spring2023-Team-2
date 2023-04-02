import datetime as dt

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


def setup_oppboard_tests(test_case):
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
    """
    test_case.org = Organization.objects.create(
        user=User.objects.create(
            email="jedi@jedi.com",
            password="peace_and_justice_for_the_galaxy",
            type=UserType.ORGANIZATION,
        ),
        name="Jedi Council",
    )
    test_case.category = Category.objects.create(name="Environment")
    test_case.subcategory = Subcategory.objects.create(
        name="Conservation", parent=test_case.category
    )
    test_case.subsubcategory = Subsubcategory.objects.create(
        name="Reforestation", parent=test_case.subcategory
    )
    description = "Please help us support our community at this week's soup kitchen"
    test_case.end = dt.time(1, 30, 0)
    test_case.date = dt.datetime(year=2023, month=5, day=8, tzinfo=dt.timezone.utc)
    delta = dt.timedelta(days=30)
    test_case.end_date = test_case.date + delta
    test_case.opp = Opportunity.objects.create(
        organization=test_case.org,
        category=test_case.category,
        subcategory=test_case.subcategory,
        subsubcategory=test_case.subsubcategory,
        title="Cloud City Soup Kitchen",
        description=description,
        date=test_case.date,
        end=test_case.end,
        address_1="200 Calrissian Av.",
        address_2="NY",
        longitude=12.34,
        latitude=56.78,
        staffing=9,
        is_published=False,
        is_recurring=True,
        recurrence="weekly",
        end_date=test_case.end_date,
    )
