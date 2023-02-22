from django.urls import path

from . import views

app_name = 'organization_profile'
urlpatterns = [
    # Profiles
    path('<int:organ_id>', views.organization_profile, name='organization_profile'),
]