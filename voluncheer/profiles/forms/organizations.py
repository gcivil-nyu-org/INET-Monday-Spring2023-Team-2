import logging

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OrganizationCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = UserType.ORGANIZATION
        if commit:
            user.save()
            Organization.objects.create(
                user=user,
                name=self.cleaned_data.get("name"),
                photo=self.cleaned_data.get("photo"),
            )
        return user


class OrganizationChangeForm(UserChangeForm):
    """This form is for edit organization profile."""

    password = None

    class Meta(UserChangeForm.Meta):
        model = Organization
        fields = (
            "name",
            "website",
            "photo",
            "description",
        )

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        organization = Organization.objects.get(pk=user)
        if self.is_valid():
            organization.name = self.cleaned_data.get("name")
            organization.photo = self.cleaned_data.get("photo")
            organization.website = self.cleaned_data.get("website")
            organization.description = self.cleaned_data.get("description")
            organization.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(self.errors)
