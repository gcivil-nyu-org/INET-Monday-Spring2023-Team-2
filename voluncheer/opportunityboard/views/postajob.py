from django.http import Http404
from django.shortcuts import render, redirect

from opportunityboard.forms.postajob import PostAnOpportunityForm


def post_a_job(request):
    if request.user.is_anonymous:
        return redirect("home")
    if request.method == "POST":
        form = PostAnOpportunityForm(request.POST, instance=request.user)
        if form.is_valid():
            """create a new Opportunity and save it to the db"""
            form.save()

            return redirect("home")
    opportunity_form = PostAnOpportunityForm(instance=request.user)
    return render(
        request,
        "opportunityboard/postaopportunity.html",
        {"opportunity_form": opportunity_form},
    )
