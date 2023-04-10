from django.urls import path

from chatroom.views import chat_homepage_view
from chatroom.views import room_view

urlpatterns = [
    path("", chat_homepage_view, name="chat_homepage"),
    path("<str:room_name>/", room_view, name="room"),
]
