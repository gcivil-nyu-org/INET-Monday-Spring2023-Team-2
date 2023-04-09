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
    @transaction.atomic
    def handle(self, *args, **options):
        json_data = open("profiles/fixtures/badge_data.json")
        data = json.load(json_data)

        for row in data:
            # Create a new Badge object for each item in the dataset
            try:
                badge, created = Badge.objects.update_or_create(
                    name=row["fields"]["name"],
                    type=row["fields"]["type"],
                    img=row["fields"]["img"],
                    hours_required=parse_time(row["fields"]["hours_required"]),
                )

            except KeyError:
                pass
