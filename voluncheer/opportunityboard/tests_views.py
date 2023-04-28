import datetime

from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.urls import reverse
import freezegun

from opportunityboard.models import Category
from opportunityboard.unittest_setup import TestCase
from opportunityboard.views.opportunityboard import deregister_volunteer
from opportunityboard.views.opportunityboard import opportunityboard
from opportunityboard.views.opportunityboard import signup_volunteer
from opportunityboard.views.search import Filter
from profiles.models import UserType
from profiles.models import Volunteer


class OpportunityboardTestCase(TestCase):
    """Test cases for Opportunityboard view"""

    def test_opportunityboard_page_loads(self):
        """Tests opportunityboard page loads"""
        response = self.client.get(reverse("opportunityboard", args=[1]))
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
        get_request = rf.get(
            "/opportunityboard/search",
            {
                "category": "Animals",
                "duration": "<=2 Hours",
                "choices-single-defaul": "FUSION",
                "distance": "2.9",
                "startdates": "03/23/2023 - 03/23/2023",
            },
        )
        get_request.user = self.vol.user
        response = opportunityboard(get_request, 1)
        self.assertEqual(response.status_code, 200)

    def test_search_excludes_opportunities_before_now(self):
        """Tests that opportunities before now are not returned."""
        with freezegun.freeze_time(self.date + datetime.timedelta(days=1)):
            filters = Filter()
            self.assertEqual(filters.search().count(), 0)

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
            self.opp.end = datetime.time(2, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over two hours"):
            self.opp.end = datetime.time(2, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_lte4hrs(self):
        """Test that selecting "4 hours or less" returns opportunities with correct duration"""
        filters = Filter(duration="4 hours or less")
        opp_pk = self.opp.pk

        with self.subTest("four hours"):
            self.opp.end = datetime.time(4, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over four hours"):
            self.opp.end = datetime.time(4, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_duration_lte8hrs(self):
        """Test that selecting "Full-day" returns opportunities with correct duration"""
        filters = Filter(duration="Full-day")
        opp_pk = self.opp.pk

        with self.subTest("eight hours"):
            self.opp.end = datetime.time(8, 0, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertTrue(opp_list.filter(pk=opp_pk).exists())

        with self.subTest("over eight hours"):
            self.opp.end = datetime.time(8, 1, 0)
            self.opp.save()
            opp_list = filters.search()
            self.assertFalse(opp_list.filter(pk=opp_pk).exists())

    def test_search_by_distance(self):
        filters = Filter(latitude=40.752133, longitude=-73.984776)

        with self.subTest("within_distance"):
            filters.distance = 3
            self.opp.save()
            opp_list = filters.search()
            self.assertEqual(len(opp_list), 1)

        with self.subTest("outside_distance"):
            filters.distance = 2
            self.opp.save()
            opp_list = filters.search()
            self.assertEqual(len(opp_list), 0)


class VolunteerSignUpView(TestCase):
    """This is the test case for Volunteer signup and other volunteer centric behaviors"""

    def setUp(self):
        super().setUp()

    def test_signup_volunteer(self):
        rf = RequestFactory()
        test_request = rf.request()
        test_request.user = self.vol.user
        signup_volunteer(test_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.staffing, 8)

    def test_deregister_volunteer(self):
        rf = RequestFactory()
        test_request = rf.request()
        test_request.user = self.vol.user
        deregister_volunteer(test_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.staffing, 9)
        signup_volunteer(test_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.staffing, 8)
        deregister_volunteer(test_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.staffing, 9)


class OrganizationViewTestCase(TestCase):
    """This is the test case for Volunteer-side Organization view"""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            email="test@voluncheer.com",
            password="secret",
            type=UserType.VOLUNTEER,
        )
        self.user.save()
        self.client.login(email="test@voluncheer.com", password="secret")
        self.vol2 = Volunteer.objects.create(
            user=self.user,
            first_name="Luke",
            last_name="Skywalker",
            date_of_birth="1955-09-25",
        ).save()

    def test_organization_view(self):
        """test volunteer can visit organization profiles"""
        response = self.client.get(reverse("organization_view", args=[self.org.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "volunteer/vol_org_view.html")
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["organization"], self.org)
        self.assertQuerysetEqual(
            response.context["recurring_posted_opportunity_lists"],
            ["Cloud City Soup Kitchen"],
            transform=lambda x: str(x),
            ordered=False,
        )
