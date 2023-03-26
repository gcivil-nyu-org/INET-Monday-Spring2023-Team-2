from django.shortcuts import render

from voluncheer import settings


def map(request):
    """Renders a Google Maps view."""
    context = {"key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "voluncheer/map.html", context)
