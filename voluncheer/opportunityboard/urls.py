from django.urls import path

from opportunityboard.views.opportunityboard import opportunityboard
from opportunityboard.views.opportunityboard import select
from opportunityboard.views.postanopportunity import post_an_opportunity

urlpatterns = [
    path("", opportunityboard, name="opportunityboard"),
    # Opportunityboard
    path("select", select, name="select"),
    # Post an Opportunity
    path("post", post_an_opportunity, name="post_an_opportunity"),
]
