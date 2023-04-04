# Create your tests here.

from django.test import TestCase,override_settings
from django.urls import reverse
from voluncheer import settings

@override_settings(ALLOW_ANONYMOUS=True)
class ChatroomViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.settings(ALLOW_ANONYMOUS=True)
        
    @override_settings(ALLOW_ANONYMOUS=True)
    def test_chat_homepage_loads(self):
        with self.settings(ALLOW_ANONYMOUS=True):
            """Tests chat homepage loads"""
            response = self.client.get(reverse("chat_homepage"))
            print(response)
            self.assertEqual(response.status_code, 200)
            
    def test_room_loads(self):
        """Tests room loads"""
        response = self.client.get(reverse("room"))
        self.assertEqual(response.status_code, [200,302])