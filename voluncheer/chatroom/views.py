from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chatroom.models import Room
import voluncheer.settings as settings

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
    room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "chatroom/room.html",
        {
            "room": room,
        },
    )
