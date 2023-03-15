from django.test import TestCase

from profiles.forms.volunteers import VolunteerCreationForm
from profiles.forms.organizations import OrganizationCreationForm
from profiles.forms.organizations import OrganizationChangeForm
from profiles.forms.volunteers import VolunteerChangeForm


class OrganizationCreationFormTest(TestCase):
    """Test cases for Organization Creation form"""

    def setUp(self):
        """See base class."""
        self.form = OrganizationCreationForm()
        self.data1 = {
            "name": "Sith Lords",
            "email": "sith@sith.com",
            "password1": "come_to_the_dark_side",
            "password2": "come_to_the_dark_side",
            "type": "UserType.ORGANIZATION,",
        }
        self.form1 = OrganizationCreationForm(data=self.data1)
        self.form1.save(self)

    def test_name_label(self):
        """Test name field is labeled correctly"""
        tempLabel = self.form.fields["name"].label
        self.assertTrue(tempLabel is None or tempLabel == "Name")

    def test_organization_must_submit_unique_email(self):
        """Test that organization email must be unique"""
        data2 = {
            "name": "The Sith Lords",
            "email": "sith@sith.com",
            "password1": "come_to_the_dark_side_again",
            "password2": "come_to_the_dark_side_again",
            "type": "UserType.ORGANIZATION,",
        }
        self.assertTrue(self.form1.is_valid())
        form2 = OrganizationCreationForm(data=data2)
        self.assertFalse(form2.is_valid())

    def test_organization_can_add_photo(self):
        """Test that organization can add photo"""
        data2 = {
            "name": "The Sith Lords",
            "email": "sith@sith.com",
            "password1": "come_to_the_dark_side_again",
            "password2": "come_to_the_dark_side_again",
            "type": "UserType.ORGANIZATION,",
            "photo": "sith-lord.jpg",
        }
        self.assertIsNone(self.form1.data.get("photo"))
        # No default photo displayed
        form2 = OrganizationChangeForm(data=data2)
        # assert that the photo has been changed
        self.assertEqual(form2.data["photo"], "sith-lord.jpg")


class VolunteerCreationFormTest(TestCase):
    """Test cases for Volunteer Creation form"""

    def setUp(self):
        """See base class."""
        self.form = VolunteerCreationForm()
        data1 = {
            "first_name": "Han",
            "last_name": "Solo",
            "date_of_birth": "1942-07-13",
            "email": "millenium@falcon.com",
            "password1": "ch3wb@cc@",
            "password2": "ch3wb@cc@",
            "type": "UserType.VOLUNTEER,",
        }
        self.form1 = VolunteerCreationForm(data=data1)
        self.form1.save(self)

    def test_first_name_label(self):
        """Test first name field is labeled correctly"""
        tempLabel = self.form.fields["first_name"].label
        self.assertTrue(tempLabel is None or tempLabel == "First Name")

    def test_last_name_label(self):
        """Test last name field is labeled correctly"""
        tempLabel = self.form.fields["last_name"].label
        self.assertTrue(tempLabel is None or tempLabel == "Last Name")

    def test_date_of_birth_label(self):
        """Test dob field is labeled correctly"""
        tempLabel = self.form.fields["date_of_birth"].label
        self.assertTrue(tempLabel is None or tempLabel == "Date Of Birth")

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

    def test_volunteer_must_submit_unique_email(self):
        """Test that volunteer email must be unique"""
        data2 = {
            "first_name": "Harrison",
            "last_name": "Ford",
            "date_of_birth": "1942-07-13",
            "email": "millenium@falcon.com",
            "password1": "ch3wb@cc@",
            "password2": "ch3wb@cc@",
            "type": "UserType.VOLUNTEER,",
        }
        self.assertTrue(self.form1.is_valid())
        form2 = VolunteerCreationForm(data=data2)
        self.assertFalse(form2.is_valid())

    def test_volunteer_can_add_photo(self):
        """Test that volunteer can add photo"""
        data2 = {
            "first_name": "Harrison",
            "last_name": "Ford",
            "date_of_birth": "1942-07-13",
            "email": "millenium@falcon.com",
            "password1": "ch3wb@cc@",
            "password2": "ch3wb@cc@",
            "type": "UserType.VOLUNTEER,",
            "photo": "sith-lord.jpg",
        }
        self.assertIsNone(self.form1.data.get("photo"))
        # No default photo displayed
        form2 = VolunteerChangeForm(data=data2)
        # assert that the photo has been changed
        self.assertEqual(form2.data["photo"], "sith-lord.jpg")
