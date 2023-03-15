from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db import transaction

from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer

import logging


_is_alpha = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Only upper and lower case English alphabet characters are allowed.",  # noqa: E501
)


class VolunteerCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, validators=[_is_alpha])
    last_name = forms.CharField(required=True, validators=[_is_alpha])
    date_of_birth = forms.DateField(required=True)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = UserType.VOLUNTEER
        if commit:
            user.save()
        Volunteer.objects.create(
            user=user,
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            photo=self.cleaned_data.get("photo"),
        )

        return user


""" VolunteerChangeForm

This form is for edit volunteer profile.
"""


class VolunteerChangeForm(UserChangeForm):
    password = None
    photo = forms.ImageField(required=False)

    class Meta(UserChangeForm.Meta):
        model = Volunteer
        fields = ("first_name", "last_name", "date_of_birth", "photo")

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        volunteer = Volunteer.objects.get(pk=user)

        if self.is_valid():
            volunteer.first_name = self.cleaned_data.get("first_name")
            volunteer.last_name = self.cleaned_data.get("last_name")
            volunteer.date_of_birth = self.cleaned_data.get("date_of_birth")
            volunteer.photo = self.cleaned_data.get("photo")
            volunteer.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(self.errors)
