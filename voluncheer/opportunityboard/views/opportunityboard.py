from django.apps import apps
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

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


def signup_volunteer(request, opportunity_id):

    # get opportunity
    opportunity = Opportunity.objects.get(pk=opportunity_id)

    # add user to opportunity

    # delete these print statements, just for verification
    print(opportunity_id)
    print(request.user)

    return HttpResponseRedirect(reverse("opportunityboard"))
