from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('ws/chatroom/welcome', consumers.GroupGuestConsumer.as_asgi()),
  path('ws/chatroom/echo', consumers.EchoConsumer.as_asgi()),
]
