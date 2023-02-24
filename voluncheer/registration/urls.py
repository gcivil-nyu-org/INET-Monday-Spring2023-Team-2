from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('', views.registration_form.as_view(), name='registration'),
]