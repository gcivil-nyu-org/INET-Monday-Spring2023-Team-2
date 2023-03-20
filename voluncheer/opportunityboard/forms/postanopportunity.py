from django import forms
from django.utils import timezone

from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory
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
    end = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        ),
    )

    class Meta:
        model = Opportunity

        fields = (
            "title",
            "category",
            "subcategory",
            "subsubcategory",
            "description",
            "staffing",
            "date",
            "end",
            "address_1",
            "address_2",
            "is_published",
            "photo",
        )

        labels = {"subcategory": "Subcategory 1", "subsubcategory": "Subcategory 2"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subcategory"].queryset = Subcategory.objects.none()
        self.fields["subsubcategory"].queryset = Subsubcategory.objects.none()

        if "category" in self.data:
            try:
                parent_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    parent_id=parent_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

        if "subcategory" in self.data:
            try:
                parent_id = int(self.data.get("subcategory"))
                self.fields["subsubcategory"].queryset = Subsubcategory.objects.filter(
                    parent_id=parent_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

    def save(self, commit=True):
        user = self.instance
        organization = Organization.objects.get(pk=user)
        if self.is_valid():
            opportunity = Opportunity()
            opportunity.pubdate = timezone.now()
            opportunity.organization = organization
            opportunity.category = self.cleaned_data.get("category")
            opportunity.subcategory = self.cleaned_data.get("subcategory")
            opportunity.subsubcategory = self.cleaned_data.get("subsubcategory")
            opportunity.title = self.cleaned_data.get("title")
            opportunity.description = self.cleaned_data.get("description")
            opportunity.staffing = self.cleaned_data.get("staffing")
            opportunity.date = self.cleaned_data.get("date")
            opportunity.end = self.cleaned_data.get("end")
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
