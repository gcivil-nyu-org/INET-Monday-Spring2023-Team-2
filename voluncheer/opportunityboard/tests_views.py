import datetime as dt

from django.test.client import RequestFactory
from django.urls import reverse

from opportunityboard.models import Category
from opportunityboard.unittest_setup import TestCase
from opportunityboard.views.search import Filter
from opportunityboard.views.search import filter_search


class OpportunityboardTestCase(TestCase):
    """Test cases for Opportunityboard view"""

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
        """Test that selecting "2 hours or less" returns opportunities with correct duration"""
        filters = Filter(duration="2 hours or less")
        opp_pk = self.opp.pk

        with self.subTest("two hours"):
            self.opp.end = dt.time(2, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over two hours"):
            self.opp.end = dt.time(2, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_lte4hrs(self):
        """Test that selecting "4 hours or less" returns opportunities with correct duration"""
        filters = Filter(duration="4 hours or less")
        opp_pk = self.opp.pk

        with self.subTest("four hours"):
            self.opp.end = dt.time(4, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over four hours"):
            self.opp.end = dt.time(4, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_lte8hrs(self):
        """Test that selecting "Full-day" returns opportunities with correct duration"""
        filters = Filter(duration="Full-day")
        opp_pk = self.opp.pk

        with self.subTest("eight hours"):
            self.opp.end = dt.time(8, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over eight hours"):
            self.opp.end = dt.time(8, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())
