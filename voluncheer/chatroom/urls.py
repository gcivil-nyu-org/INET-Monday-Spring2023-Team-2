from chatroom.views import chat_homepage_view, room_view
from django.urls import path

urlpatterns = [
    path("", chat_homepage_view, name="chat_homepage"),
    path("<str:room_name>/", room_view, name="room"),
]
