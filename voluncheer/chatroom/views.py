from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from chatroom.models import Message
from chatroom.models import Room

# To be changed after UI is designed.


@login_required
def chat_homepage_view(request):
    return render(
        request,
        "chatroom/chat_homepage.html",
        {
            "rooms": Room.objects.all(),
        },
    )


@login_required
def room_view(request, room_name):
    room, _ = Room.objects.get_or_create(name=room_name)
    message = Message.objects.filter(room=room)

    return render(
        request,
        "chatroom/room.html",
        {
            "message": message,
            "rooms": Room.objects.all(),
            "room": room,
        },
    )
