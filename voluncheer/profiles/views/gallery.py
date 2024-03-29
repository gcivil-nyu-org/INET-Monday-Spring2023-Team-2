from django.shortcuts import redirect
from django.shortcuts import render

from profiles.forms.gallery import CreateGalleryPostForm
from profiles.models import Volunteer


def create_post(request):
    """create a new Post and save it to the database."""
    user = request.user
    if user.is_anonymous or user.is_organization:
        return redirect("home")
    if user.is_volunteer:
        volunteer_profile = Volunteer.objects.get(pk=user)
    if request.method == "POST":
        post = request.POST.copy()
        post.update({"volunteer": volunteer_profile})
        request.POST = post
        form = CreateGalleryPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(target_volunteer=volunteer_profile)
        else:
            return render(
                request,
                "profiles/posttogallery.html",
                {"gallerypost_form": form},
            )
        return redirect("home")
    else:
        form = CreateGalleryPostForm()
        return render(
            request,
            "profiles/posttogallery.html",
            {"gallerypost_form": form, "volunteer": volunteer_profile},
        )


def delete_post(request, post_id):
    form = CreateGalleryPostForm()
    form.delete(post_id)
    return redirect("home")
