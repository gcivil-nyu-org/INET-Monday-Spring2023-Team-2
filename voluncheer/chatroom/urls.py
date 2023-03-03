from django.urls import path

from . import views

app_name = "chatroom"
urlpatterns = [
    # Chatroom
    path(
        "user_profile/<int:user_id>/chatroom",
        views.chatroom_user,
        name="chatroom_user",
    ),
    path(
        "organization_profile/<int:organ_id>/chatroom",
        views.chatroom_organ,
        name="chatroom_organ",
    ),
]
