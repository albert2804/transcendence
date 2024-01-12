# remote_game/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^endpoint/remoteGame/$', consumers.RemoteGameConsumer.as_asgi()),
]