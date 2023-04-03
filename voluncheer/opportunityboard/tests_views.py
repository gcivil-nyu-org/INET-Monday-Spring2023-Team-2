from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.utils import timezone

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.views.opportunityboard import deregister_volunteer
from opportunityboard.views.opportunityboard import signup_volunteer
from opportunityboard.views.search import Filter
from opportunityboard.views.search import filter_search
from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer


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
        end = "12:00:00"
        self.date = timezone.now()
        self.soup = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Cloud City Soup Kitchen",
            description=description,
            date=self.date,
            end=end,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_published=True,
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
        response = self.client.get(reverse("update_an_opportunity", args=[self.soup.pk]))
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


class VolunteerSignUpView(TestCase):
    """This is the test case for Volunteer signup and other volunteer centric behaviors"""

    def setUp(self):
        super().setUp()
        self.luke = Volunteer.objects.create(
            user=User.objects.create(
                email="luke@jedi.com",
                password="NOOOOOOOOOOOOOOOOOOO",
                type=UserType.VOLUNTEER,
            ),
            first_name="Luke",
            last_name="Skywalker",
            date_of_birth="1955-09-25",
            description="I want to come with you to Alderaan.",
        )
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
        end = "12:00:00"
        self.date = timezone.now()
        self.soup = Opportunity.objects.create(
            organization=self.org,
            category=self.category,
            subcategory=self.subcategory,
            subsubcategory=self.subsubcategory,
            title="Cloud City Soup Kitchen",
            description=description,
            date=self.date,
            end=end,
            address_1="200 Calrissian Av.",
            address_2="NY",
            longitude=12.34,
            latitude=56.78,
            staffing=9,
            is_published=True,
        )

    def test_signup_volunteer(self):
        rf = RequestFactory()
        test_request = rf.request()
        test_request.user = self.luke.user
        signup_volunteer(test_request, self.soup.pk)
        self.soup.refresh_from_db()
        self.assertEqual(self.soup.staffing, 8)

    def test_deregister_volunteer(self):
        rf = RequestFactory()
        test_request = rf.request()
        test_request.user = self.luke.user
        deregister_volunteer(test_request, self.soup.pk)
        self.soup.refresh_from_db()
        self.assertEqual(self.soup.staffing, 9)
        signup_volunteer(test_request, self.soup.pk)
        self.soup.refresh_from_db()
        self.assertEqual(self.soup.staffing, 8)
        deregister_volunteer(test_request, self.soup.pk)
        self.soup.refresh_from_db()
        self.assertEqual(self.soup.staffing, 9)
