from django.urls import path

from . import views

app_name = 'map'
urlpatterns = [
    # Map
    path('', views.map, name='map'),
]