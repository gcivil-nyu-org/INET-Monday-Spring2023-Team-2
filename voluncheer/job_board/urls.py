from django.urls import path

from job_board import views

app_name = 'job_board'
urlpatterns = [
    path('', views.jobboard, name='jobboard'),

    # Jobboard
    path('select', views.jobboard_select, name='select'),
]