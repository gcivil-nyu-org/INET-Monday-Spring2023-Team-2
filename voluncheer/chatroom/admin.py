from django.contrib import admin

from chatroom.models import Message
from chatroom.models import Room

admin.site.register(Room)
admin.site.register(Message)
