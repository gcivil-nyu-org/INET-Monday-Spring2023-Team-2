from django.urls import path

from jobboard.views.jobboard import jobboard, select
from jobboard.views.postajob import post_a_job


urlpatterns = [
    path("", jobboard, name="jobboard"),
    # Jobboard
    path("select", select, name="select"),
    # Post a Job
    path("post_a_job", post_a_job, name="post_a_job"),
]
