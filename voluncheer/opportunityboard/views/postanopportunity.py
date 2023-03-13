from django.http import Http404
from django.shortcuts import render, redirect

from opportunityboard.forms.postanopportunity import PostAnOpportunityForm


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
