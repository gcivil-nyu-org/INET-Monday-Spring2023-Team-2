from django import forms

user_choices = [("cyr","Choose your role"),("volunteer","Volunteer"),
                ("organization","Organization")]
 
# creating a form
class InputForm(forms.Form):
    
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    age = forms.IntegerField(max_value=100, min_value=13)
    role= forms.CharField(widget=forms.Select(choices=user_choices))
    email = forms.CharField(max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput())
