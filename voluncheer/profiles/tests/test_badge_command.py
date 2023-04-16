from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from profiles.models import Badge

_TEST_DATA = "profiles/testdata/badges.json"


class TestLoadBadgeDataCommandTest(TestCase):
    def test_badge_details(self):
        """Test that load_badge_data command creates default badges"""
        out = StringIO()
        call_command("load_badge_data", badge_data=_TEST_DATA, stdout=out)
        self.assertTrue(Badge.objects.filter(name="Test Badge 1").exists())
        self.assertTrue(Badge.objects.filter(name="Test Badge 2").exists())
        self.assertIn("Successfully created 'Test Badge 1'.", out.getvalue())
        self.assertIn("Successfully created 'Test Badge 2'.", out.getvalue())

        with self.subTest("test_already_exist_does_not_create_new_badges"):
            exists_out = StringIO()
            call_command("load_badge_data", badge_data=_TEST_DATA, stdout=exists_out)
            self.assertNotIn(
                "Successfully created 'Test Badge 1'.", exists_out.getvalue()
            )
            self.assertNotIn(
                "Successfully created 'Test Badge 2'.", exists_out.getvalue()
            )
            self.assertEqual(len(Badge.objects.all()), 2)
