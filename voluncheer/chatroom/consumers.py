import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chatroom.models import Message
from chatroom.models import Room
from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def save_message(self, user, room, content, timestamp):
        user = User.objects.get(pk=user)
        volunteer = None
        organization = None
        if user.is_organization:
            organization = Organization.objects.get(pk=user)
        elif user.is_volunteer:
            volunteer = Volunteer.objects.get(pk=user)
        else:
            return
        room = Room.objects.get(name=room)
        Message.objects.create(
            user=user,
            room=room,
            content=content,
            timestamp=timestamp,
            organization=organization,
            volunteer=volunteer,
        )

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = Room.objects.get(name=self.room_name)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data, bytes_data=None):
        test_data_json = json.loads(text_data)
        content = test_data_json["message"]
        user = test_data_json["user"]
        room = test_data_json["room"]
        timestamp = test_data_json["timestamp"]
        photo = test_data_json["photo"]
        self.save_message(user, room, content, timestamp)
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": content,
                "photo": photo,
            },
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
