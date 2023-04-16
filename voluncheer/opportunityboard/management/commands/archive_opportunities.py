from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
import pytz

from opportunityboard.models import Opportunity


class Command(BaseCommand):
    help = "Archive opportunities that have ended"

    def add_arguments(self, parser):
        parser.add_argument(
            "--datetime",
            default=datetime.now(pytz.utc),
            help="The date before which all opportunities are archived",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        now = options["datetime"]

        opportunities = Opportunity.objects.filter(
            date__lte=now,
            is_recurring=False,
            is_archived=False,
            is_published=True,
        )

        for opportunity in opportunities:
            # Set is_archived to True if end date and time has passed
            end_datetime = datetime.combine(opportunity.date.date(), opportunity.end).replace(
                tzinfo=pytz.utc
            )
            if end_datetime <= now:
                opportunity.is_archived = True
                opportunity.save()
