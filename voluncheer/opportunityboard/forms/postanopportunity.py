from django import forms
from django.utils import timezone

from opportunityboard.models import Opportunity
from profiles.models import Organization


class PostAnOpportunityForm(forms.ModelForm):
    """This is the form used for creating a new opportunity for organization users."""

    date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )
    duration = forms.DurationField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        ),
    )

    class Meta:
        model = Opportunity
        fields = (
            "category",
            "title",
            "description",
            "date",
            "duration",
            "address_1",
            "address_2",
            "is_published",
            "photo",
        )

    def save(self, commit=True):
        user = self.instance
        organization = Organization.objects.get(pk=user)
        if self.is_valid():
            opportunity = Opportunity()
            opportunity.pubdate = timezone.now()
            opportunity.organization = organization
            opportunity.category = self.cleaned_data.get("category")
            opportunity.title = self.cleaned_data.get("title")
            opportunity.description = self.cleaned_data.get("description")
            opportunity.date = self.cleaned_data.get("date")
            opportunity.duration = self.cleaned_data.get("duration")
            opportunity.address_1 = self.cleaned_data.get("address_1")
            opportunity.address_2 = self.cleaned_data.get("address_2")
            opportunity.is_published = self.cleaned_data.get("is_published")
            opportunity.photo = self.cleaned_data.get("photo")
            opportunity.save()

    def update(self, opportunity_id):
        opportunity = Opportunity.objects.get(pk=opportunity_id)
        if self.is_valid():
            opportunity.category = self.cleaned_data.get("category")
            opportunity.title = self.cleaned_data.get("title")
            opportunity.description = self.cleaned_data.get("description")
            opportunity.date = self.cleaned_data.get("date")
            opportunity.duration = self.cleaned_data.get("duration")
            opportunity.address_1 = self.cleaned_data.get("address_1")
            opportunity.address_2 = self.cleaned_data.get("address_2")
            opportunity.is_published = self.cleaned_data.get("is_published")
            opportunity.photo = self.cleaned_data.get("photo")
            opportunity.save()

    def delete(self, opportunity_id):
        Opportunity.objects.filter(pk=opportunity_id).delete()
