from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db import transaction

from profiles.models import User
from profiles.models import UserType
from profiles.models import Volunteer

_is_alpha = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Only upper and lower case English alphabet characters are allowed.",
)


class VolunteerCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, validators=[_is_alpha])
    last_name = forms.CharField(required=True, validators=[_is_alpha])
    date_of_birth = forms.DateField(required=True)

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
        )
        return user