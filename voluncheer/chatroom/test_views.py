import random
import string

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from profiles.models import UserType


class ChatroomViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.password = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )
        self.user = get_user_model().objects.create_user(
            email="test@voluncheer.com",
            password="secret",
            type=UserType.VOLUNTEER,
        )
        self.user.save()
        self.client.login(email="test@voluncheer.com", password="secret")

    def tearDown(self):
        self.user.delete()

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
