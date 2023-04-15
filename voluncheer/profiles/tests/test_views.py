from django.test.client import RequestFactory
from django.urls import reverse

from opportunityboard.unittest_setup import TestCase
from profiles.models import GalleryPost
from profiles.views.gallery import create_post
from profiles.views.profile import confirm_attendance


class SignupViewTest(TestCase):
    """Test cases for Signup view"""

    def test_signup_form_accessible_by_name(self):
        """Tests accessing signup form for volunteers by name"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_exists_at_desired_location(self):
        """Tests accessing  signup form by URL"""
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_form_uses_correct_template(self):
        """Tests sign up view uses correct template"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")


class VolunteerSignUpViewTest(TestCase):
    """Test cases for Volunteer Signup view"""

    def test_volunteer_signup_form_accessible_by_name(self):
        """Tests accessing signup form for volunteers by name"""
        response = self.client.get(reverse("volunteer_signup"))
        self.assertEqual(response.status_code, 200)

    def test_volunteer_signup_form_exists_at_desired_location(self):
        """Tests accessing signup form for volunteers by URL"""
        response = self.client.get("/accounts/signup/volunteer/")
        self.assertEqual(response.status_code, 200)

    def test_volunteer_signup_form_correct_template(self):
        """Tests volunteer sign up view uses correct template"""
        response = self.client.get(reverse("volunteer_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup_form.html")


class OrganizationSignUpViewTest(TestCase):
    """Test cases for Organization Signup view"""

    def test_organization_signup_form_accessible_by_name(self):
        """Tests accessing signup form for organizations by name"""
        response = self.client.get(reverse("organization_signup"))
        self.assertEqual(response.status_code, 200)

    def test__organization_signup_form_exists_at_desired_location(self):
        """Tests accessing signup form for organizations by URL"""
        response = self.client.get("/accounts/signup/organization/")
        self.assertEqual(response.status_code, 200)

    def test_organization_signup_form_uses_correct_template(self):
        """Tests organization sign up view uses correct template"""
        response = self.client.get(reverse("organization_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup_form.html")


class HomeViewTest(TestCase):
    """Test cases for Home view"""

    def test_home_accessible_by_name(self):
        """Tests accessing signup form for volunteers by name"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_exists_at_desired_location(self):
        """Tests accessing home by URL"""
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)


class OrganizationProfileTest(TestCase):
    """Test cases for Organization profile based functions"""

    def test_confirm_attendance(self):
        """Test the confirm attendance feature.
        The request here is for mimicing the get request of select a volunteer and submit.
        The first confirm_attendance call won't work since volunteer is not signed up.
        The second confirm_attendance call will add the volunteer to attended_volunteers.
        The third confirm_attendance call will remove the volunteer from attended_volunteers.
        """
        rf = RequestFactory()
        get_request = rf.get(
            f"/attendance/{self.opp.pk}",
            {"volunteer-attended": [str(self.vol.pk)]},
        )
        get_request.user = self.org

        confirm_attendance(get_request, self.opp.pk)
        self.assertEqual(self.opp.attended_volunteers.count(), 0)

        self.opp.volunteers.add(self.vol)
        self.opp.refresh_from_db()
        confirm_attendance(get_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.attended_volunteers.count(), 1)

        confirm_attendance(get_request, self.opp.pk)
        self.opp.refresh_from_db()
        self.assertEqual(self.opp.attended_volunteers.count(), 0)


class GalleryTest(TestCase):
    """Test cases for Gallery based functions"""

    def test_create_post(self):
        """test create gallery post function"""
        rf = RequestFactory()
        get_request = rf.post(
            "profile/post/",
            {"title": ["Blah"], "content": ["Boooooooo"]},
        )
        get_request.user = self.vol.user

        self.assertEqual(GalleryPost.objects.all().count(), 0)
        create_post(get_request)
        self.assertEqual(GalleryPost.objects.all().count(), 1)

    def test_delete_post(self):
        """test delete gallery post function"""
        new_post = GalleryPost.objects.create(
            volunteer=self.vol, author=self.vol, title="Booo", content="Hoooo"
        )
        self.assertEqual(GalleryPost.objects.all().count(), 1)
        self.client.get(reverse("delete_post", args=[new_post.pk]))
        self.assertEqual(GalleryPost.objects.all().count(), 0)
