from django.apps import apps
from django.shortcuts import render

from opportunityboard.models import Opportunity

Organization = apps.get_model("profiles", "Organization")


def opportunityboard(request):
    """View for Opportunity Board"""
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    context = {"opportunity_lists": opportunity_lists}
    return render(request, "voluncheer/opportunityboard.html", context)


def select(request):
    """Placeholder view for later use"""
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    context = {"opportunity_lists": opportunity_lists}
    return render(request, "voluncheer/opportunityboard.html", context)
