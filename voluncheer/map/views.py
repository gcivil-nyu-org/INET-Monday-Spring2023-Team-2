from django.shortcuts import render

from map import models
from opportunityboard.models import Opportunity
from voluncheer import settings


def map(request):
    """Renders a Google Maps view."""
    organizations = []
    for organization in models.NYCharities.objects.all():
        if "," in organization.type:
            tokens = organization.type.split(",", maxsplit=1)
            organization_type = f"{tokens[0].strip()} ({tokens[1].strip()})"
        else:
            organization_type = organization.type
        organizations.append(
            {
                "name": organization.name,
                "address": organization.address,
                "latitude": organization.latitude,
                "longitude": organization.longitude,
                "type": organization_type,
            },
        )

    opportunities = []
    for opportunity in Opportunity.objects.all():
        if opportunity.is_published and not opportunity.is_archived:
            if opportunity.latitude and opportunity.longitude:
                opportunities.append(
                    {
                        "latitude": opportunity.latitude,
                        "longitude": opportunity.longitude,
                        "title": opportunity.title,
                        "address": opportunity.address_1,
                        "type": opportunity.category.name,
                        "name": opportunity.organization.name,
                    }
                )

    context = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "organizations": organizations,
        "opportunities": opportunities,
    }
    return render(request, "voluncheer/map.html", context)
