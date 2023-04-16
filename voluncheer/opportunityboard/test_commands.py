from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from opportunityboard.models import Category, Subcategory, Subsubcategory

_TEST_DATA = "opportunityboard/testdata/categories.json"

_CATEGORY = "Test Category"
_SUB_CATEGORY = "Test Sub Category"
_SUB_SUB_CATEGORY = "Test Sub Sub Category"


class TestLoadCategories(TestCase):
    """Tests the load categories command."""

    def test_load_categories(self):
        out = StringIO()
        call_command("load_categories", category_data=_TEST_DATA, stdout=out)
        self.assertTrue(Category.objects.filter(name=_CATEGORY).exists())
        self.assertTrue(Subcategory.objects.filter(name=_SUB_CATEGORY).exists())
        self.assertTrue(Subsubcategory.objects.filter(name=_SUB_SUB_CATEGORY).exists())

        self.assertIn("Successfully created 'Test Category'.", out.getvalue())
        self.assertIn("Successfully created 'Test Sub Category'.", out.getvalue())
        self.assertIn("Successfully created 'Test Sub Sub Category'.", out.getvalue())

        with self.subTest("test_already_exist_does_not_create_new_categories"):
            exists_out = StringIO()
            call_command("load_categories", category_data=_TEST_DATA, stdout=exists_out)
            self.assertNotIn(
                "Successfully created 'Test Category'.", exists_out.getvalue()
            )
            self.assertNotIn(
                "Successfully created 'Test Sub Category'.", exists_out.getvalue()
            )
            self.assertNotIn(
                "Successfully created 'Test Sub Sub Category'.", exists_out.getvalue()
            )

            self.assertEqual(len(Category.objects.all()), 1)
            self.assertEqual(len(Subcategory.objects.all()), 1)
            self.assertEqual(len(Subsubcategory.objects.all()), 1)
