from django import forms
from django.utils import timezone

from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory


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
            "organization",
            "title",
            "category",
            "subcategory",
            "subsubcategory",
            "description",
            "staffing",
            "date",
            "end",
            "is_recurring",
            "recurrence",
            "end_date",
            "occurences",
            "address_1",
            "address_2",
            "is_published",
            "photo",
        )

        labels = {
            "subcategory": "Subcategory 1",
            "subsubcategory": "Subcategory 2",
            "is_recurring": "Recurring opportunity?",
        }

        widgets = {
            "organization": forms.HiddenInput(),
        }

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
        elif self.instance.pk:
            try:
                self.fields[
                    "subcategory"
                ].queryset = self.instance.category.subcategory_set.order_by("name")
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
        elif self.instance.pk:
            try:
                self.fields[
                    "subsubcategory"
                ].queryset = self.instance.subcategory.subsubcategory_set.order_by("name")
            except (ValueError, TypeError, AttributeError):
                pass

    def save(self, *args, **kwargs):
        if self.is_valid():
            super().save(*args, **kwargs)

    def delete(self, opportunity_id):
        Opportunity.objects.filter(pk=opportunity_id).delete()
