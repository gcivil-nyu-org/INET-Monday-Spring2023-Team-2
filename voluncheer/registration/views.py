from django.shortcuts import render
from .forms import InputForm
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView, FormView
 
# ======================== Registration ============================
class registration_form(CreateView):
    form_class = InputForm
    template_name = 'voluncheer/registration.html'
    success_url = '/login/'
    
