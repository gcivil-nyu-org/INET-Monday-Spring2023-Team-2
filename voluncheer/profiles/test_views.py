from django.test import TestCase
from django.urls import reverse


class SignupViewTest(TestCase):
    """Test cases for Signup view"""

    def test_signup_form_accessible_by_name(self):
        """Tests accessing signup form for volunteers by name"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_exists_at_desired_location(self):
        """Tests accessing  signup form by URL"""
        response = self.client.get("/signup/")
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
        response = self.client.get("/signup/volunteer/")
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

    def test_organization_signup_form_exists_at_desired_location(self):
        """Tests accessing signup form for organizations by URL"""
        response = self.client.get("/signup/organization/")
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
