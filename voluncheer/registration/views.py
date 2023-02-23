from django.shortcuts import render
from .forms import InputForm
from django.http import HttpResponse
from django.template import loader
 
# Create your views here.
def registration_view(request):
    context ={}
    context['form']= InputForm()
    return render(request, "voluncheer/registration.html", context)
