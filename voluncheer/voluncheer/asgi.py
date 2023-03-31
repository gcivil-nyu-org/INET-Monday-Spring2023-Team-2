"""
ASGI config for voluncheer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application

import chatroom.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voluncheer.settings")
application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': URLRouter(
      chatroom.routing.websocket_urlpatterns
    ),
})
