from django.shortcuts import redirect
from django.shortcuts import render

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from opportunityboard.models import Subcategory, Subsubcategory


def post_an_opportunity(request):
    """create a new Opportunity and save it to the database."""
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        if request.user.is_anonymous:
            return render(request, "opportunityboard/postanopportunity.html", {})

        opportunity_form = PostAnOpportunityForm(instance=request.user)
        return render(
            request,
            "opportunityboard/postanopportunity.html",
            {"opportunity_form": opportunity_form},
        )


def load_subcategories(request):
    """Request all subcategories for a given category to populate drop-down"""
    category_id = request.GET.get("category")
    if category_id:
        subcategories = Subcategory.objects.filter(parent=category_id).order_by("name")
    else:  # drop-down changed to empty field
        subcategories = {}
    return render(
        request,
        "opportunityboard/subcategory_dropdown_list_options.html",
        {"subcategories": subcategories},
    )


def load_subsubcategories(request):
    """Request all subsubcategories for a given subcategory to populate drop-down"""
    subcategory_id = request.GET.get("subcategory")
    if subcategory_id:
        subsubcategories = Subsubcategory.objects.filter(parent=subcategory_id).order_by("name")
    else:  # drop-down changed to empty field
        subsubcategories = {}
    return render(
        request,
        "opportunityboard/subsubcategory_dropdown_list_options.html",
        {"subsubcategories": subsubcategories},
    )
