import datetime as dt

from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.unittest_setup import TestCase
from opportunityboard.views.opportunityboard import deregister_volunteer
from opportunityboard.views.opportunityboard import opportunityboard
from opportunityboard.views.opportunityboard import signup_volunteer
from opportunityboard.views.search import Filter
from profiles.models import Organization
from profiles.models import User


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
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(password="testpass", email="xyz@xyz.com", type=2)
        self.organization = Organization.objects.create(name="Test Organization", user=self.user)
        self.category = Category.objects.create(name="Sports")
        self.subcategory = Subcategory.objects.create(name="Farmwork", parent=self.category)
        self.subsubcategory = Subsubcategory.objects.create(name="Feeding", parent=self.subcategory)
        self.opportunity1 = Opportunity.objects.create(
            organization=self.organization,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Test Opportunity",
            description="Test description",
            date=dt.datetime.now() + dt.timedelta(days=1),
            end=dt.datetime.now().time(),
            address_1="Test address 1",
            address_2="Test address 2",
            longitude="55.5555",
            latitude="44.4444",
            staffing=5,
            is_published=True,
        )

    # self.opportunity2 = Opportunity.objects.create(
    #     title="Test Opportunity 2", organization=self.organization, date=dt.date(2023, 11, 4))

    def test_organization_view(self):
        # login = self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("organization_view", args=[self.organization.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "volunteer/vol_org_view.html")
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["organization"], self.organization)
        print(response.context["opportunity_lists"])
        self.assertQuerysetEqual(
            response.context["opportunity_lists"],
            ["Test Opportunity"],
            transform=lambda x: str(x),
            ordered=False
        )
