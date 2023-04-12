from django import forms
from django.db import transaction

from profiles.models import GallaryPost


class CreateGalleryPostForm(forms.ModelForm):
    """This is the form used for creating a new post for volunteer gallery."""

    class Meta:
        model = GallaryPost
        fields = (
            "title",
            "photo",
            "content",
        )

    @transaction.atomic
    def save(self, target_volunteer):
        if self.is_valid():
            GallaryPost.objects.create(
                volunteer=target_volunteer,
                author=self.data.get("volunteer"),
                title=self.cleaned_data.get("title"),
                photo=self.cleaned_data.get("photo"),
                content=self.cleaned_data.get("content"),
            )

    def delete(self, post_pk):
        GallaryPost.objects.filter(pk=post_pk).delete()
