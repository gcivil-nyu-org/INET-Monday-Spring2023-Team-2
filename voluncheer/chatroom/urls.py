from django.contrib import admin
from django.urls import re_path,path, include
from chatroom.views import chatroom
urlpatterns = [
    re_path("profile/<int:user_id>/chatroom", chatroom, name="chatroom"),
]