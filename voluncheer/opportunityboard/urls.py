from django.urls import path
from opportunityboard.views.opportunityboard import (
    deregister_volunteer,
    opportunityboard,
    organization_view,
    signup_volunteer,
)
from opportunityboard.views.postanopportunity import (
    load_subcategories,
    load_subsubcategories,
    post_an_opportunity,
    update_an_opportunity,
)

urlpatterns = [
    # Opportunityboard
    path("<int:page_number>", opportunityboard, name="opportunityboard"),
    # Post an Opportunity
    path("post", post_an_opportunity, name="post_an_opportunity"),
    # Get subcategories
    path(
        "ajax/load-subcategories/", load_subcategories, name="ajax_load_subcategories"
    ),
    # Get subsubcategories
    path(
        "ajax/load-subsubcategories/",
        load_subsubcategories,
        name="ajax_load_subsubcategories",
    ),
    # Update an Opportunity
    path(
        "update/<int:opportunity_id>",
        update_an_opportunity,
        name="update_an_opportunity",
    ),
    # Filter Search
    path("search", opportunityboard, name="filter_search"),
    # Volunteer Signup
    path(
        "signup_volunteer/<int:opportunity_id>",
        signup_volunteer,
        name="signup_volunteer",
    ),
    # Volunteer Deregister
    path(
        "deregister_volunteer/<int:opportunity_id>",
        deregister_volunteer,
        name="deregister_volunteer",
    ),
    path("profile/<int:userid>", organization_view, name="organization_view"),
]
