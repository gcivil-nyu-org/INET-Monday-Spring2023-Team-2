from django.shortcuts import redirect
from django.shortcuts import render

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
from profiles.models import Organization


def post_an_opportunity(request):
    """create a new Opportunity and save it to the database."""
    user = request.user
    if user.is_anonymous:
        return redirect("home")
    if user.is_organization:
        organization_profile = Organization.objects.get(pk=user)
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors.as_data())
        return redirect("home")

    else:
        opportunity_form = PostAnOpportunityForm(instance=request.user)
        return render(
            request,
            "opportunityboard/postanopportunity.html",
            {"opportunity_form": opportunity_form, "organization": organization_profile},
        )


def update_an_opportunity(request, opportunity_id):
    """Get opportunity update POST and call save function on ChangeForms."""
    user = request.user
    if user.is_anonymous:
        return redirect("home")
    if user.is_organization:
        organization_profile = Organization.objects.get(pk=user)
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.update(opportunity_id)
        else:
            print(form.errors.as_data())
        return redirect("home")
    else:
        opportunity_form = PostAnOpportunityForm(instance=request.user)
        return render(
            request,
            "opportunityboard/updateanopportunity.html",
            {
                "opportunity_form": opportunity_form,
                "organization": organization_profile,
                "opportunity_id": opportunity_id,
            },
        )


def load_subcategories(request):
    """Request all subcategories for a given category to populate drop-down"""
    category_id = request.GET.get("category")
    if category_id:
        subcategories = Subcategory.objects.filter(parent=category_id).order_by("name")
        subsubcategories = Subsubcategory.objects.none()
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
