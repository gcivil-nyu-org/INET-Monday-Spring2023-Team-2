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
    category = post.get("category")
    category = category_is_valid(category)
    output["category"] = category

    return output


def category_is_valid(value):
    """Check if the category is valid
    Input: value[category_name] -> string
    Return: error(None), target_object
    """
    category = Category.objects.filter(name=value).first()
    if category is not None:
        return category
    subcategory = Subcategory.objects.filter(name=value).first()
    if subcategory is not None:
        return subcategory
    subsubcategory = Subsubcategory.objects.filter(name=value).first()
    if subsubcategory is not None:
        return subsubcategory
    return None
