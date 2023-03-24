from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from map.models import NYCharities
import requests


class Command(BaseCommand):
    help = "Pull data from NYC Open Data and save to NYCharities table"

    @transaction.atomic
    def handle(self, *args, **options):
        url = "https://data.cityofnewyork.us/resource/yunp-vs8g.json"

        response = requests.get(url)

        if response.status_code != 200:
            raise CommandError("Could not pull data from NYC Open Data")

        # Clear NYCharities table before inserting new data
        NYCharities.objects.all().delete()

        data = response.json()
        for row in data:
            # Create a new NYCharities object for each item in the dataset
            try:
                nycharity = NYCharities(
                    name=row["organization_city_agency"],
                    street=row["street_address_mailing_address"],
                    city=row["city"],
                    state=row["state"],
                    type=row["organization_type"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                )
                nycharity.save()
            except KeyError:
                pass
