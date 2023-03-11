from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from profiles.models import Organization

from jobboard.models import Job


class PostAJobForm(forms.ModelForm):
    """This is the form used for creating a new job for organization users"""

    class Meta:
        model = Job
        fields = (
            "category",
            "title",
            "description",
            # "date",
            # "duration",
            "address_1",
            "address_2",
            "is_published",
        )

    def save(self, commit=True):
        user = self.instance
        organization = Organization.objects.get(pk=user)
        if self.is_valid():
            job = Job()
            job.pubdate = timezone.now()
            job.organization = organization
            job.category = self.cleaned_data.get("category")
            job.title = self.cleaned_data.get("title")
            job.description = self.cleaned_data.get("description")
            # job.date = self.cleaned_data.get("date")
            # job.duration = self.cleaned_data.get("duration")
            job.address_1 = self.cleaned_data.get("address_1")
            job.address_2 = self.cleaned_data.get("address_2")
            job.is_published = self.cleaned_data.get("is_published")
            job.save()
