from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from chatroom.models import Room
import voluncheer.settings as settings

# To be changed after UI is designed.


def chat_homepage_view(request):
    print("settings.Allow annoymous is", settings.ALLOW_ANONYMOUS)
    if (not request.user.is_authenticated) and settings.ALLOW_ANONYMOUS is False:
        return redirect_to_login(request.path)
    print("did not redirect")
    return render(
        request,
        "chatroom/chat_homepage.html",
        {
            "rooms": Room.objects.all(),
        },
    )


def room_view(request, room_name):
    if (not request.user.is_authenticated) and settings.ALLOW_ANONYMOUS is False:
        return redirect_to_login(request.path)
    room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "chatroom/room.html",
        {
            "room": room,
        },
    )
