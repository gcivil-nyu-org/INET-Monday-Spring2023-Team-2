import logging

from django.shortcuts import render

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.views.opportunityboard import category_dict_gen


def filter_search(request):
    if request.method == "POST":
        filter = parse_search_filter(request.POST)
        logger = logging.getLogger(__name__)
        logger.error(filter)
        opportunity_lists = search_by_filters(filter)
    else:
        opportunity_lists = Opportunity.objects.order_by("-pubdate"[:20])
    cate_output_dict = category_dict_gen()
    durations = {
        "One-day": ["<=2 Hours", "2-4 Hours", "Full Day"],
    }
    context = {
        "opportunity_lists": opportunity_lists,
        "categories": cate_output_dict,
        "durations": durations,
    }
    return render(request, "voluncheer/opportunityboard.html", context)


def parse_search_filter(post):
    """Check if the input filters are valid:
    category(default empty string)
    duration(default empty string)
    distance(default 0)
    """
    output = {}
    # Category filter
    value = post.get("category")
    category = category_is_valid(value)
    output["category"] = category
    subcategory = subcategory_is_valid(value)
    output["subcategory"] = subcategory
    subsubcategory = subsubcategory_is_valid(value)
    output["subsubcategory"] = subsubcategory

    return output


def category_is_valid(value):
    """Check if the category is valid
    Input: value[category_name] -> string
    Return: None or category
    """
    category = Category.objects.filter(name=value).first()
    return category


def subcategory_is_valid(value):
    """Check if the subcategory is valid"""
    subcategory = Subcategory.objects.filter(name=value).first()
    return subcategory


def subsubcategory_is_valid(value):
    """Check if the subsubcategory is valid"""
    subsubcategory = Subsubcategory.objects.filter(name=value).first()
    return subsubcategory


def search_by_filters(filter):
    """Search by the given filters
    Input: filter dictionary
    category(no-filter: None)
    subcategory(no-filter: None)
    subsubcategory(no-filter: None)
    Output: Opportunity list
    """
    filtered_opportunity = Opportunity.objects.all()
    if filter["category"] is not None:
        filtered_opportunity = filtered_opportunity.filter(category=filter["category"])
    if filter["subcategory"] is not None:
        filtered_opportunity = filtered_opportunity.filter(subcategory=filter["subcategory"])
    if filter["subsubcategory"] is not None:
        filtered_opportunity = filtered_opportunity.filter(subsubcategory=filter["subsubcategory"])

    return filtered_opportunity
