import datetime

from django import forms
from django.core.exceptions import ValidationError

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
        required=True,
    )
    end = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        ),
    )

    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
        required=False,
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
            if self.cleaned_data.get("is_recurring"):
                date = self.cleaned_data.get("date")
                end_date = self.cleaned_data.get("end_date")
                for i in range(12):
                    if date.date() > end_date:
                        break
                    self.instance.pk = None
                    self.instance.save()
                    date += datetime.timedelta(days=7)
                    self.instance.date = date
                self.find_siblings()
            else:
                super().save(*args, **kwargs)

    def edit(self, *args, **kwargs):
        if self.is_valid():
            super().save(*args, **kwargs)

    def find_siblings(self):
        siblings = Opportunity.objects.filter(
            title=self.instance.title,
            is_recurring=self.instance.is_recurring,
            end_date=self.instance.end_date,
            is_archived=False,
        )
        for sibling in siblings:
            sibling.recurrence_siblings.add(*siblings.exclude(pk=sibling.pk))

    def delete(self, opportunity_id):
        Opportunity.objects.filter(pk=opportunity_id).delete()

    def delete_recurrences(self, opportunity_id):
        opportunity = Opportunity.objects.get(pk=opportunity_id)
        opportunity.delete_recurrences()

    def clean(self):
        super(PostAnOpportunityForm, self).clean()
        is_recurring = self.cleaned_data.get("is_recurring")
        recurrence = self.cleaned_data.get("recurrence")

        if is_recurring and not recurrence:
            raise ValidationError("Must enter recurrence if opportunity is recurring")

        date = self.cleaned_data.get("date")
        if date < datetime.datetime.now(tz=date.tzinfo):
            raise ValidationError("Start date and time must be in the future.")
        start_time = date.time()
        end_time = self.cleaned_data.get("end")

        if start_time >= end_time:
            raise ValidationError("End time must be after start time")

        return self.cleaned_data
