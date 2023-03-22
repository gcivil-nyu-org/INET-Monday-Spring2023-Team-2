from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm
from profiles.models import Organization
from opportunityboard.models import Opportunity


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
    obj = get_object_or_404(Opportunity, pk=opportunity_id)
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            if "delete" in request.POST:
                form.delete(opportunity_id)
            else:
                form.update(opportunity_id)
        else:
            print(form.errors.as_data())
        return redirect("home")
    else:
        opportunity_form = PostAnOpportunityForm(instance=obj)
        return render(
            request,
            "opportunityboard/updateanopportunity.html",
            {
                "opportunity_form": opportunity_form,
                "organization": organization_profile,
                "opportunity_id": opportunity_id,
            },
        )
