import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from map.models import NYCharities


class Command(BaseCommand):
    help = "Pull data from NYC Open Data and save to NYCharities table"

    @transaction.atomic
    def handle(self, *args, **options):
        url = "https://data.cityofnewyork.us/resource/yunp-vs8g.json"

        response = requests.get(url)

        if response.status_code != 200:
            raise CommandError("Could not pull data from NYC Open Data")

        data = response.json()
        for row in data:
            # Create a new NYCharities object for each item in the dataset
            try:
                nycharity, created = NYCharities.objects.update_or_create(
                    name=row["organization_city_agency"],
                    type=row["organization_type"],
                    bin_num=row["bin"],
                    defaults={
                        "street": row["street_address_mailing_address"],
                        "city": row["city"],
                        "state": row["state"],
                        "zip_code": row["postcode"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                    },
                )

            except KeyError:
                pass
