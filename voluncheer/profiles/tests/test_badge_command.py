from datetime import timedelta
from django.core.management import call_command
from django.test import TestCase

from profiles.models import Badge


class TestLoadBadgeDataCommandTest(TestCase):
    def setUp(self):
        call_command("load_badge_data")

    def test_badge_details(self):
        """Test that load_badge_data command creates default badges"""
        badges = Badge.objects.all()
        self.assertEqual(len(badges), 4)
        gold_badge = Badge.objects.get(name="Gold")
        self.assertEqual(gold_badge.name, "Gold")
        self.assertEqual(gold_badge.type, 0)
        bronze_badge = Badge.objects.get(name="Bronze")
        self.assertEqual(str(bronze_badge.img), "badges/bronze_badge.jpeg")
        self.assertEqual(bronze_badge.hours_required, timedelta(hours=10))
