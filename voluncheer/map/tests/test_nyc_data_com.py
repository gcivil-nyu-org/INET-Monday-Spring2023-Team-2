from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
import requests

from map.models import NYCharities


class TestNYCharitiesCommandTest(TestCase):
    def setUp(self):
        self.test_data = [
            {
                "organization_city_agency": "Test Charity 1",
                "organization_type": "Environment",
                "street_address_mailing_address": "123 Tree St",
                "city": "New York",
                "state": "NY",
                "latitude": "40.1234",
                "longitude": "-73.5678",
            },
            {
                "organization_city_agency": "Test Charity 2",
                "organization_type": "Animals",
                "street_address_mailing_address": "456 Animals St",
                "city": "New York",
                "state": "NY",
                "latitude": "40.5678",
                "longitude": "-73.1234",
            },
            {
                "organization_city_agency": "Test Charity 3",
                "organization_type": "Community",
                "street_address_mailing_address": "456 Test Street",
                "city": "New York",
                "state": "NY",
            },
        ]

    @patch.object(requests, "get")
    def test_command(self, mock_get):
        mock_get.return_value.json.return_value = self.test_data
        mock_get.return_value.status_code = 200

        call_command("pull_nyc_charities")

        charities = NYCharities.objects.all()
        self.assertEqual(len(charities), 2)
        self.assertEqual(charities[0].name, "Test Charity 1")
        self.assertEqual(charities[1].name, "Test Charity 2")
        self.assertEqual(charities[0].latitude, 40.1234)
        self.assertEqual(charities[0].longitude, -73.5678)
