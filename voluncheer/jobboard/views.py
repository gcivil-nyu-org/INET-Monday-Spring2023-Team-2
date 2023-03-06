from django.shortcuts import render
from django.apps import apps

from jobboard.models import Job

Organization = apps.get_model("profiles", "Organization")

# ======================== Job Board ============================


def jobboard(request):
    job_lists = Job.objects.order_by("-pubdate"[:20])
    context = {"job_lists": job_lists}
    return render(request, "voluncheer/jobboard.html", context)


def select(request):
    job_lists = Job.objects.order_by("-pubdate"[:20])
    context = {"job_lists": job_lists}
    return render(request, "voluncheer/jobboard.html", context)
