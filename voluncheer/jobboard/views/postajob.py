from django.shortcuts import render, redirect

from jobboard.forms.postajob import PostAJobForm


def post_a_job(request):
    if request.method == "POST":
        form = PostAJobForm(request.POST, instance=request.user)
        if form.is_valid():
            """create a new Job and save it to the db"""
            form.save()

            return redirect("home")
    else:
        job_form = PostAJobForm(instance=request.user)
        return render(request, "jobboard/postajob.html", {"job_form": job_form})
