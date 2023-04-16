"""The load_categories command injects missing categories into the database."""

import json

from django.core.management.base import BaseCommand

from opportunityboard.models import Category
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory

# JSON model type representations.
_CATEGORY = "opportunityboard.category"
_SUB_CATEGORY = "opportunityboard.subcategory"
_SUB_SUB_CATEGORY = "opportunityboard.subsubcategory"


class Command(BaseCommand):
    help = "Loads missing categories for the opportunity board."

    def add_arguments(self, parser):
        parser.add_argument(
            "--category_data",
            default="opportunityboard/fixtures/category_data.json",
            help="The path to the data (in JSON format).",
        )

    def handle(self, *args, **options):
        del args  # Unused.
        with open(options["category_data"]) as raw_data:
            data = json.loads(raw_data.read())

        for entry in data:
            if entry["model"] == _CATEGORY:
                model = Category
            elif entry["model"] == _SUB_CATEGORY:
                model = Subcategory
            elif entry["model"] == _SUB_SUB_CATEGORY:
                model = Subsubcategory
            else:
                continue

            name = entry["fields"]["name"]
            if model.objects.filter(name=name).exists():
                continue

            model.objects.create(**entry["fields"])
            self.stdout.write(self.style.SUCCESS(f"Successfully created {repr(name)}."))
