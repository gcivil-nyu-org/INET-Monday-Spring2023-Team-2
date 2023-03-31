from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from chatroom.models import Room


# To be changed after UI is designed.
def chat_homepage_view(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.path)
    return render(
        request,
        "chatroom/chat_homepage.html",
        {
            "rooms": Room.objects.all(),
        },
    )


def room_view(request, room_name):
    if not request.user.is_authenticated:
        return redirect_to_login(request.path)
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "chatroom/room.html",
        {
            "room": chat_room,
        },
    )
