from django.test import Client
from django.test import TestCase
from django.urls import reverse

from map import urls
from map import views


class MapTestCase(TestCase):
    def test_page_loads(self):
        c = Client()
        for url in urls.urlpatterns:
            appNameAndUrl =urls.app_name+":"+url.name
            response = c.get(reverse(appNameAndUrl))
            self.assertEqual(response.status_code, 200)
