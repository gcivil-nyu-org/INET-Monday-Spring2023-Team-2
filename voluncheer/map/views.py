from django.shortcuts import render

from map import models
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
    context = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "organizations": organizations,
    }
    return render(request, "voluncheer/map.html", context)
