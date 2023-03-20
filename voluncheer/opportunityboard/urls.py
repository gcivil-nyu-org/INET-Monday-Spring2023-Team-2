from django.urls import path

from opportunityboard.views.opportunityboard import opportunityboard
from opportunityboard.views.opportunityboard import select
from opportunityboard.views.postanopportunity import load_subcategories
from opportunityboard.views.postanopportunity import load_subsubcategories
from opportunityboard.views.postanopportunity import post_an_opportunity
from opportunityboard.views.postanopportunity import update_an_opportunity

urlpatterns = [
    path("", opportunityboard, name="opportunityboard"),
    # Opportunityboard
    path("select", select, name="select"),
    # Post an Opportunity
    path("post", post_an_opportunity, name="post_an_opportunity"),
    # Get subcategories
    path("ajax/load-subcategories/", load_subcategories, name="ajax_load_subcategories"),
    # Get subsubcategories
    path("ajax/load-subsubcategories/", load_subsubcategories, name="ajax_load_subsubcategories"),
    # Update an Opportunity
    path("update/<int:opportunity_id>", update_an_opportunity, name="update_an_opportunity"),
]
