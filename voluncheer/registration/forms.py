from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
 
# creating a form
class InputForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'first_name', 'last_name', 'date_of_birth', 'email', 'password']
    

