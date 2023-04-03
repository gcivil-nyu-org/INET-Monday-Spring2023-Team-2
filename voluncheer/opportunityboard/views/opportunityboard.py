import json

from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.views.search import parse_search_filter
from profiles.models import Volunteer

Organization = apps.get_model("profiles", "Organization")
OPPORTUNITY_PER_PAGE = 5


def opportunityboard(request, page_number):
    """View for Opportunity Board"""
    filter = parse_search_filter(request.GET)
    opportunity_lists = filter.search()
    number_of_pages = (opportunity_lists.count() // OPPORTUNITY_PER_PAGE) + 1
    opportunity_lists = opportunity_lists.order_by("-pubdate")[
        (page_number - 1) * OPPORTUNITY_PER_PAGE : page_number * OPPORTUNITY_PER_PAGE
    ]
    cate_output_dict = category_dict_gen()
    durations = {
        "One-day": ["2 hours or less", "4 hours or less", "Full-day"],
    }
    context = {
        "range_of_pages": range(1, number_of_pages + 1),
        "curr_page": page_number,
        "opportunity_lists": opportunity_lists,
        "categories": cate_output_dict,
        "durations": durations,
        "filter": json.dumps(filter.gen_dict()),
        "category_placeholder": filter.gen_category_placeholder(),
        "duration_placeholder": filter.gen_duration_placeholder(),
    }
    if not request.user.is_anonymous and request.user.is_volunteer:
        context["volunteer"] = Volunteer.objects.get(pk=request.user)
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
    volunteer = get_object_or_404(Volunteer, pk=request.user.pk)
    opportunity = Opportunity.objects.get(pk=opportunity_id)
    if opportunity.staffing > 0 and volunteer not in opportunity.volunteers.all():
        opportunity.volunteers.add(volunteer)
        opportunity.staffing -= 1
        opportunity.save()
    return HttpResponseRedirect(reverse("opportunityboard", args=[1]))


def deregister_volunteer(request, opportunity_id):
    volunteer = get_object_or_404(Volunteer, pk=request.user.pk)
    opportunity = Opportunity.objects.get(pk=opportunity_id)
    if volunteer in opportunity.volunteers.all():
        opportunity.volunteers.remove(volunteer)
        opportunity.staffing += 1
        opportunity.save()
    return HttpResponseRedirect(reverse("opportunityboard", args=[1]))
