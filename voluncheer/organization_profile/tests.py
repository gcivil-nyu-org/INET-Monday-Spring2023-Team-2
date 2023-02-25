from django.test import TestCase
from django.test import Client
from . import urls,views
from django.urls import reverse
import pytest
from . import models

# Create your tests here.
class OrganizationProfileTestCase(TestCase):
    def setUp(self):
        models.Organization.objects.create(id='1',organization_name="testOrg")
    
    @pytest.mark.django_db
    def test_page_loads(self):
        c = Client()
        for url in urls.urlpatterns:
            appNameAndUrl=urls.app_name+":"+url.name
            response = c.get(reverse(appNameAndUrl,args=[1]))
            self.assertEqual(response.status_code, 200)