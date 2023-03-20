from django.test import TestCase
from django.urls import reverse


class OpportunityboardTestCase(TestCase):
    """Test cases for Opportunityboard view"""

    def test_opportunityboard_page_loads(self):
        """Tests opportunityboard page loads"""
        response = self.client.get(reverse("opportunityboard"))
        self.assertEqual(response.status_code, 200)

    def test_select_page_loads(self):
        """Tests select page loads"""
        response = self.client.get(reverse("select"))
        self.assertEqual(response.status_code, 200)

    def test_post_an_opportunity_page_loads(self):
        """Tests post_an_opportunity page loads"""
        response = self.client.get(reverse("post_an_opportunity"))
        self.assertIn(response.status_code, [200, 302])

    def test_update_an_opportunity_page_loads(self):
        """Tests update_an_opportunity page loads"""
        response = self.client.get(reverse("update_an_opportunity", args=[1]))
        self.assertIn(response.status_code, [200, 302])
