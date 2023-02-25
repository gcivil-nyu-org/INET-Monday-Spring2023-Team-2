from django.test import TestCase
from django.test import Client
from . import urls,views
from django.urls import reverse

# Create your tests here.
class LoginTestCase(TestCase):
    def test_page_loads(self):
        c = Client()
        for url in urls.urlpatterns:
            appNameAndUrl=urls.app_name+":"+url.name
            response = c.get(reverse(appNameAndUrl))
            self.assertEqual(response.status_code, 200)

