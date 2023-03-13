from datetime import datetime

from django.test import TestCase

from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer
from profiles.forms.volunteers import VolunteerCreationForm
from profiles.forms.volunteers import VolunteerChangeForm
from profiles.forms.organizations import OrganizationCreationForm
from profiles.forms.organizations import OrganizationChangeForm


class OrganizationCreationFormTest(TestCase):
    """Test cases for Organization Creation form"""

    def setUp(self):
        """See base class."""
        self.form = OrganizationCreationForm()

    def test_name_label(self):
        """Test name field is labeled correctly"""
        self.assertTrue(
            self.form.fields["name"].label is None
            or self.form.fields["name"].label == "Name"
        )

    def test_organization_must_submit_unique_email(self):
        """Test that organization email must be unique"""
        data1 = {
            "name": "Sith Lords",
            "email": "sith@sith.com",
            "password1": "come_to_the_dark_side",
            "password2": "come_to_the_dark_side",
            "type": "UserType.ORGANIZATION,",
        }
        data2 = {
            "name": "The Sith Lords",
            "email": "sith@sith.com",
            "password1": "come_to_the_dark_side_again",
            "password2": "come_to_the_dark_side_again",
            "type": "UserType.ORGANIZATION,",
        }

        form1 = OrganizationCreationForm(data=data1)
        self.assertTrue(form1.is_valid())
        form1.save(self)  # Submitting form 1
        form2 = OrganizationCreationForm(data=data2)
        self.assertFalse(form2.is_valid())


class VolunteerCreationFormTest(TestCase):
    """Test cases for Volunteer Creation form"""

    def setUp(self):
        """See base class."""
        self.form = VolunteerCreationForm()

    def test_first_name_label(self):
        """Test first name field is labeled correctly"""
        self.assertTrue(
            self.form.fields["first_name"].label is None
            or self.form.fields["first_name"].label == "First Name"
        )

    def test_last_name_label(self):
        """Test last name field is labeled correctly"""
        self.assertTrue(
            self.form.fields["last_name"].label is None
            or self.form.fields["last_name"].label == "Last Name"
        )

    def test_date_of_birth_label(self):
        """Test dob field is labeled correctly"""
        self.assertTrue(
            self.form.fields["date_of_birth"].label is None
            or self.form.fields["date_of_birth"].label == "Date of Birth"
        )

    def test_name_validation(self):
        """Test volunteers cannot have numbers in first_name"""
        data = {
            "first_name": "R2D2",
            "last_name": "Robot",
            "date_of_birth": "2000-01-01",
            "email": "r2d2@jedi.com",
            "password1": "beep_boop",
            "password2": "beep_boop",
            "type": "UserType.VOLUNTEER",
        }
        form = VolunteerCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_organization_must_submit_unique_email(self):
        """Test that volunteer email must be unique"""
        data1 = {
            "first_name": "Han",
            "last_name": "Solo",
            "date_of_birth": "1942-07-13",
            "email": "millenium@falcon.com",
            "password1": "ch3wb@cc@",
            "password2": "ch3wb@cc@",
            "type": "UserType.VOLUNTEER,",
        }
        data2 = {
            "first_name": "Harrison",
            "last_name": "Ford",
            "date_of_birth": "1942-07-13",
            "email": "millenium@falcon.com",
            "password1": "ch3wb@cc@",
            "password2": "ch3wb@cc@",
            "type": "UserType.VOLUNTEER,",
        }

        form1 = VolunteerCreationForm(data=data1)
        self.assertTrue(form1.is_valid())
        form1.save(self)  # Submitting form 1
        form2 = VolunteerCreationForm(data=data2)
        self.assertFalse(form2.is_valid())


class VolunteerChangeFormTest(TestCase):
    """Test cases for Volunteer Change form"""

    def setUp(self):
        """See base class."""
        self.form = VolunteerChangeForm()
        self.user = Volunteer.objects.create(
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
        self.user.save()

    def test_validation(self):
        """Test volunteer profile update validation"""
        self.assertNotEqual(self.user.first_name, "R2D2")
        self.assertNotEqual(self.user.last_name, "Robot")
        self.assertNotEqual(
            self.user.date_of_birth, datetime.strptime("2000-01-01", "%Y-%m-%d").date()
        )
        self.assertNotEqual(self.user.badges, "badge-2,badge-4")
        self.assertNotEqual(self.user.description, "beep_boop")
        data = {
            "first_name": "R2D2",
            "last_name": "Robot",
            "date_of_birth": "2000-01-01",
            "badges": "badge-2,badge-4",
            "description": "beep_boop",
        }
        form = VolunteerChangeForm(data=data, instance=self.user)
        self.assertFalse(form.save())
        self.assertEqual(self.user.first_name, "R2D2")
        self.assertEqual(self.user.last_name, "Robot")
        self.assertEqual(
            self.user.date_of_birth, datetime.strptime("2000-01-01", "%Y-%m-%d").date()
        )
        self.assertEqual(self.user.badges, "badge-2,badge-4")
        self.assertEqual(self.user.description, "beep_boop")


class OrganizationChangeFormTest(TestCase):
    """Test cases for Organization Change form"""

    def setUp(self):
        """See base class."""
        self.form = OrganizationChangeForm()
        self.user = Organization.objects.create(
            user=User.objects.create(
                email="jedi@jedi.com",
                password="peace_and_justice_for_the_galaxy",
                type=UserType.ORGANIZATION,
            ),
            name="Jedi Council",
        )
        self.user.save()

    def test_validation(self):
        """Test organization profile update validation"""
        self.assertNotEqual(self.user.name, "Dije")
        self.assertNotEqual(self.user.website, "www.google.com")
        self.assertNotEqual(self.user.description, "beep_boop")
        data = {
            "name": "Dije",
            "website": "www.google.com",
            "description": "beep_boop",
        }
        form = OrganizationChangeForm(data=data, instance=self.user)
        self.assertFalse(form.save())
        self.assertEqual(self.user.name, "Dije")
        self.assertEqual(self.user.website, "www.google.com")
        self.assertEqual(self.user.description, "beep_boop")
