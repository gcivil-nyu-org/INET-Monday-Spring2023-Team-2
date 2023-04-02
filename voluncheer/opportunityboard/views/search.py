import datetime as dt
import logging

from django.shortcuts import render

from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from opportunityboard.views.opportunityboard import category_dict_gen


class Filter:
    def __init__(
        self,
        category=None,
        subcategory=None,
        subsubcategory=None,
        duration=None,
        distance=0,
        start_date=None,
    ) -> None:
        self.category = category
        self.subcategory = subcategory
        self.subsubcategory = subsubcategory
        self.duration = duration
        self.distance = distance
        self.start_date = start_date

    def gen_dict(self):
        return {
            "category": self.category,
            "subcategory": self.subcategory,
            "subsubcategory": self.subsubcategory,
            "duration": self.duration,
            "distance": self.distance,
            "start_date": self.start_date,
        }

    def gen_category_placeholder(self):
        if self.category is not None:
            return self.category
        elif self.subcategory is not None:
            return self.subcategory
        elif self.subsubcategory is not None:
            return self.subsubcategory
        return "CATEGORY"

    def gen_duration_placeholder(self):
        if self.duration is not None:
            return self.duration
        return "DURATION"

    def search(self):
        """Search by the given filters
        Input: Filter object
        category(default: None)
        subcategory(default: None)
        subsubcategory(default: None)
        Output: Opportunity list
        """
        filtered_opportunity = Opportunity.objects.all()
        if self.category is not None:
            filtered_opportunity = filtered_opportunity.filter(category=self.category)
        if self.subcategory is not None:
            filtered_opportunity = filtered_opportunity.filter(subcategory=self.subcategory)
        if self.subsubcategory is not None:
            filtered_opportunity = filtered_opportunity.filter(subsubcategory=self.subsubcategory)
        if self.duration == "2 hours or less":
            filtered_opportunity = filter_by_duration(filtered_opportunity, 2)
        if self.duration == "4 hours or less":
            filtered_opportunity = filter_by_duration(filtered_opportunity, 4)
        if self.duration == "Full-day":
            filtered_opportunity = filter_by_duration(filtered_opportunity, 8)
        return filtered_opportunity


def filter_by_duration(queryset, max):
    """
    Takes Opportunity queryset and a max number of hours.
    Returns Opportunity queryset with durations less than or equal to the max.
    """
    max_duration = dt.timedelta(hours=max)
    for opportunity in queryset:
        if opportunity.duration > max_duration:
            queryset = queryset.exclude(pk=opportunity.pk)
    return queryset


def filter_search(request):
    filter = Filter()
    filter = parse_search_filter(request.GET)
    logger = logging.getLogger(__name__)
    logger.error(filter.gen_dict())
    opportunity_lists = filter.search()
    cate_output_dict = category_dict_gen()
    durations = {
        "One-day": ["2 hours or less", "4 hours or less", "Full-day"],
    }
    context = {
        "opportunity_lists": opportunity_lists,
        "categories": cate_output_dict,
        "durations": durations,
        "category_placeholder": filter.gen_category_placeholder(),
        "duration_placeholder": filter.gen_duration_placeholder(),
    }
    return render(request, "voluncheer/opportunityboard.html", context)


def parse_search_filter(post):
    """Check if the input filters are valid:
    category(default empty string)
    duration(default empty string)
    distance(default 0)
    """
    # Category/Duration filter
    value = post.get("category")
    selected_duration = post.get("duration")
    filter = Filter(
        category=category_is_valid(value),
        subcategory=subcategory_is_valid(value),
        subsubcategory=subsubcategory_is_valid(value),
        duration=selected_duration,
    )
    return filter


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
