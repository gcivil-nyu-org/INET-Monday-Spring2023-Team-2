from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from profiles.models import Organization
from profiles.models import User
from profiles.models import UserType


class OrganizationCreationForm(UserCreationForm):
    name = forms.CharField(required=True)

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
        )
        return user

class OrganizationChangeForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        model = Organization
        fields = ("name",)

    def save(self, commit=True):
        user = self.instance
        organization = Organization.objects.get(pk=user)
        if self.is_valid():
            organization.name = self.cleaned_data.get("name")
            organization.save()