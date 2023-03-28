from django.apps import apps
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory

Organization = apps.get_model("profiles", "Organization")


def opportunityboard(request):
    """View for Opportunity Board"""
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    cate_output_dict = category_dict_gen()
    durations = {
        "One-day": ["<=2 Hours", "2-4 Hours", "Full Day"],
    }
    context = {
        "opportunity_lists": opportunity_lists,
        "categories": cate_output_dict,
        "durations": durations,
        "category_placeholder": "CATEGORY",
        "duration_placeholder": "DURATION",
    }
    return render(request, "voluncheer/opportunityboard.html", context)


def select(request):
    """Placeholder view for later use"""
    opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    context = {"opportunity_lists": opportunity_lists}
    return render(request, "voluncheer/opportunityboard.html", context)


def category_dict_gen():
    categories = Category.objects.all()
    cate_output_dict = {}
    for category in categories:
        cate_dict = {}
        subcategories = Subcategory.objects.filter(parent=category).order_by("name")
        for subcategory in subcategories:
            subsublist = []
            for subsubcategory in Subsubcategory.objects.filter(parent=subcategory).order_by(
                "name"
            ):
                subsublist.append(subsubcategory.name)
            cate_dict[subcategory.name] = subsublist
        cate_output_dict[category.name] = cate_dict
    return cate_output_dict


def signup_volunteer(request, opportunity_id):

    # get opportunity
    opportunity = Opportunity.objects.get(pk=opportunity_id)

    # add user to opportunity

    # delete these print statements, just for verification
    print(opportunity_id)
    print(request.user)

    return HttpResponseRedirect(reverse("opportunityboard"))
