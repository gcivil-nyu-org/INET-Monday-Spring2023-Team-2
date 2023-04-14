from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
import pytz

from opportunityboard.models import Opportunity


class Command(BaseCommand):
    help = "Archive opportunities that have ended"

    @transaction.atomic
    def handle(self, **kwargs):
        now = datetime.now(pytz.utc)

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
