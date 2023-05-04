import random
import string

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from opportunityboard.unittest_setup import TestCase
from profiles.models import UserType
from profiles.models import Volunteer


class ChatroomViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email="luke@jedi.com", password="NOOOOOOOOOOOOOOOOOOO")

    def test_chat_homepage_redirects(self):
        """Tests chat homepage redirects to login."""
        self.client.logout()
        response = self.client.get(reverse("chat_homepage"))
        self.assertEqual(response.status_code, 302)

    def test_chat_homepage_loads(self):
        """Tests chat homepage loads"""
        response = self.client.get(reverse("chat_homepage"))
        self.assertEqual(response.status_code, 200)

    def test_room_loads(self):
        """Tests room loads"""
        response = self.client.get(reverse("room", args=["test"]))
        self.assertEqual(response.status_code, 200)
