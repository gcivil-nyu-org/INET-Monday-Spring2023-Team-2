from chatroom.models import Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    return render(
        request,
        "chatroom/room.html",
        {
            "room": room,
        },
    )
