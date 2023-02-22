from django.urls import path

from . import views

app_name = 'user_profile'
urlpatterns = [
    # Profiles
    path('<int:user_id>', views.user_profile, name='user_profile'),
]