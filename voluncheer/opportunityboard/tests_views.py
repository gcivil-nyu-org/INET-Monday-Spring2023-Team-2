import datetime as dt

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.views.search import Filter
from opportunityboard.views.search import filter_search
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
        self.end = dt.time(10, 30, 0)
        self.date = dt.datetime(year=2023, month=5, day=8, hour=9)
        delta = dt.timedelta(days=30)
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
        response = self.client.get(reverse("update_an_opportunity", args=[self.opp.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_search(self):
        """Tests update_an_opportunity page loads"""
        rf = RequestFactory()
        post_request = rf.post(
            "/opportunityboard/search",
            {
                "category": "Animals",
                "duration": "<=2 Hours",
                "choices-single-defaul": "FUSION",
                "distance": "2.9",
                "startdates": "03/23/2023 - 03/23/2023",
            },
        )
        response = filter_search(post_request)
        self.assertEqual(response.status_code, 200)

    def test_search_by_categories(self):
        """Tests filter search by category/subcategory/subsubcategory functions"""
        filters = Filter()
        self.assertEqual(filters.search().count(), 1)
        filters.category = Category(name="Blah")
        self.assertEqual(filters.search().count(), 0)
        filters.category = self.category
        self.assertEqual(filters.search().count(), 1)
        filters.category = None
        filters.subcategory = self.subcategory
        self.assertEqual(filters.search().count(), 1)
        filters.subcategory = None
        filters.subsubcategory = self.subsubcategory
        self.assertEqual(filters.search().count(), 1)

    def test_search_by_duration_lte2hrs(self):
        """Test that selecting "0-2 Hours" returns opportunities with correct duration"""
        filters = Filter(duration="0-2 Hours")
        opp_pk = self.opp.pk

        self.opp.end = dt.time(11, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(11, 1, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_2to4hrs(self):
        """Test that selecting "2-4 Hours" returns opportunities with correct duration"""
        filters = Filter(duration="2-4 Hours")
        opp_pk = self.opp.pk

        self.opp.end = dt.time(10, 59, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(11, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(13, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(13, 1, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_4to8hrs(self):
        """Test that selecting "4-8 Hours" returns opportunities with correct duration"""
        filters = Filter(duration="4-8 Hours")
        opp_pk = self.opp.pk

        self.opp.end = dt.time(12, 59, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(13, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(17, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(17, 1, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_gte8hrs(self):
        """Test that selecting "8+ Hours" returns opportunities with correct duration"""
        filters = Filter(duration="8+ Hours")
        opp_pk = self.opp.pk

        self.opp.end = dt.time(16, 59, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertFalse(opp_list.filter(pk=opp_pk).exists())

        self.opp.end = dt.time(17, 0, 0)
        self.opp.save()
        opp_list = filters.search()
        self.assertTrue(opp_list.filter(pk=opp_pk).exists())
