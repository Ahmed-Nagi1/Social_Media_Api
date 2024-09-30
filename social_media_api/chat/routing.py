from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat-group/(?P<room_name>[-\w]+)/$", consumers.ChatGroupConsumer.as_asgi()),
]
