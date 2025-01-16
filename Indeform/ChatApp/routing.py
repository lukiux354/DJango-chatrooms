from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatRoomConsumer.as_asgi()),
]