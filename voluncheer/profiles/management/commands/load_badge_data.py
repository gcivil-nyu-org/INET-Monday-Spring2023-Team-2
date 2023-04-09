from datetime import timedelta
import json
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from profiles.models import Badge

regex = re.compile(r"P((?P<days>\d+)DT)((?P<hours>\d+)H)((?P<minutes>\d+)M)((?P<seconds>\d+)S)")


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


class Command(BaseCommand):
    help = "Loads the missing default volunteer badges."

    def add_arguments(self, parser):
        parser.add_argument(
            "--badge_data",
            default="profiles/fixtures/badge_data.json",
            help="A JSON with the default badge data",
        )

    def handle(self, *args, **options):
        del args  # Unused.
        json_data = open("profiles/fixtures/badge_data.json")
        data = json.load(json_data)

        for entry in data:
            # Create a new Badge object for each entry in the dataset
            name = entry["fields"]["name"]
            badge, created = Badge.objects.update_or_create(
                name=name,
                type=entry["fields"]["type"],
                img=entry["fields"]["img"],
                hours_required=parse_time(entry["fields"]["hours_required"]),
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully created {repr(name)}."))
