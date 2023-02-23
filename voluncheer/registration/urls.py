from django.urls import path

from . import views

app_name = 'registration'

urlpatterns = [
    path('', views.registration_view, name='registration'),
]