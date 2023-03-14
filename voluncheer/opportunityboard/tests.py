from django.test import Client
from django.test import TestCase
from django.urls import reverse

from opportunityboard import urls


class OpportunityboardTestCase(TestCase):
    def test_page_loads(self):
        c = Client()
        for url in urls.urlpatterns:
            appNameAndUrl = url.name
            response = c.get(reverse(appNameAndUrl))
            self.assertEqual(response.status_code, 200)