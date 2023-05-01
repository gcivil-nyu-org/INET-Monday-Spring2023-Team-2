from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from opportunityboard.models import Opportunity
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
        # Set Organization based on current user
        post = request.POST.copy()
        post.update({"organization": organization_profile})
        request.POST = post
        form = PostAnOpportunityForm(request.POST, request.FILES)
        # Save
        if form.is_valid():
            form.save()
        else:
            return render(
                request,
                "opportunityboard/postanopportunity.html",
                {"opportunity_form": form},
            )
        return redirect("home")

    else:
        opportunity_form = PostAnOpportunityForm()
        return render(
            request,
            "opportunityboard/postanopportunity.html",
            {"opportunity_form": opportunity_form, "organization": organization_profile},
        )


def update_an_opportunity(request, opportunity_id):
    """Get opportunity update POST and call save function on ChangeForms."""
    opportunity_to_update = get_object_or_404(Opportunity, pk=opportunity_id)
    user = request.user
    if user.is_anonymous:
        return redirect("home")
    if user.is_organization:
        organization_profile = Organization.objects.get(pk=user)
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, request.FILES, instance=opportunity_to_update)
        if form.is_valid():
            if "delete" in request.POST:
                form.delete(opportunity_id)
            elif "delete_recurrences" in request.POST:
                form.delete_recurrences(opportunity_id)
            else:
                form.edit()
        else:
            return render(
                request,
                "opportunityboard/postanopportunity.html",
                {"opportunity_form": form},
            )
        return redirect("home")
    else:
        opportunity_form = PostAnOpportunityForm(instance=opportunity_to_update)
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
        subsubcategories = Subsubcategory.objects.none()  # noqa: F841
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
