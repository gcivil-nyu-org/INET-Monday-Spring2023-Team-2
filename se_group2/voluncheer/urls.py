from django.urls import path

from . import views

app_name = 'voluncheer'
urlpatterns = [
    path('jobboard', views.jobboard, name='jobboard'),

    # Jobboard
    path('select', views.jobboard_select, name='select'),

    # Profiles
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('organization_profile/<int:organ_id>', views.organization_profile, name='organization_profile'),

    # Chatroom
    path('user_profile/<int:user_id>/chatroom', views.chatroom_user, name='chatroom_user'),
    path('organization_profile/<int:organ_id>/chatroom', views.chatroom_organ, name='chatroom_organ'),

    # Map
    path('map', views.map, name='map'),

    path('1', views.temp, name="temp"),
]

