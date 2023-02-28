from django.urls import path

from job_board import views

app_name = 'jobboard'
urlpatterns = [
    path('', views.jobboard, name='jobboard'),

    # Jobboard
    path('select', views.select, name='select'),
]