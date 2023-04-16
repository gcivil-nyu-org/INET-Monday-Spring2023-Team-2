import datetime

import freezegun
from chatroom.models import Message, Room
from django.test import TestCase
from profiles.models import User, UserType


class ChatroomTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Test Chatroom model."""
        cls.user1 = User.objects.create(
            email="jedi@jedi.com",
            password="peace_and_justice_for_the_galaxy",
            type=UserType.ORGANIZATION,
        )
        cls.user2 = User.objects.create(
            email="luke@jedi.com",
            password="NOOOOOOOOOOOOOOOOOOO",
            type=UserType.VOLUNTEER,
        )
        cls.user3 = User.objects.create(
            email="darth_vader@sith.com",
            password="i_am_your_father",
            type=UserType.VOLUNTEER,
        )
        cls.room = Room.objects.create(name="Happy Ever After")
        cls.room.signed_up_users.add(cls.user1)
        cls.room.signed_up_users.add(cls.user2)
        cls.room.online.add(cls.user2)
        cls.room.online.add(cls.user1)
        cls.time = datetime.datetime(
            year=2023, month=5, day=8, tzinfo=datetime.timezone.utc
        )
        with freezegun.freeze_time(cls.time):
            cls.message = Message.objects.create(
                user=cls.user3, room=cls.room, content="testcontent", timestamp=cls.time
            )

    def test_private(self):
        self.assertFalse(self.room.private)

    def test_name(self):
        self.assertEquals(self.room.name, "Happy Ever After")

    def test_join(self):
        self.assertEqual(self.room.get_online_count(), 2)
        self.room.join(self.user3)
        self.assertEqual(self.room.get_online_count(), 3)
        self.assertTrue(self.room.online.filter(email=self.user3.email).exists())

    def test_leave(self):
        self.assertEqual(self.room.get_online_count(), 2)
        self.room.leave(self.user2)
        self.assertEqual(self.room.get_online_count(), 1)
        self.assertFalse(self.room.online.filter(email=self.user2.email).exists())

    def test_contains_users(self):
        self.assertTrue(self.room.online.filter(email=self.user2.email).exists())
        self.assertTrue(self.room.online.filter(email=self.user1.email).exists())

    def test_timestamp_label(self):
        self.assertEquals(self.time, self.message.timestamp)

    def test_user_label(self):
        self.assertEquals(self.user3, self.message.user)

    def test_room(self):
        self.assertEquals(self.room, self.message.room)
