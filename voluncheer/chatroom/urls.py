from django.contrib import admin
from django.urls import re_path,path, include
from chatroom.views import chatroom
urlpatterns = [
    path("", chatroom, name="chatroom"),
]