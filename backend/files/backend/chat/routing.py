# routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^endpoint/chat/$', consumers.ChatConsumer.as_asgi()),
]