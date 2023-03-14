from django.apps import apps
from django.shortcuts import render

from opportunityboard.models import Opportunity

Organization = apps.get_model("profiles", "Organization")


def opportunityboard(request):
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    context = {"opportunity_lists": opportunity_lists}
    return render(request, "voluncheer/opportunityboard.html", context)


def select(request):
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    context = {"opportunity_lists": opportunity_lists}
    return render(request, "voluncheer/opportunityboard.html", context)
