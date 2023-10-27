from django.urls import re_path, path
from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/room/(?P<department>\d+)/$', consumers.ChatConsumer.as_asgi()),
# ]

# websocket_urlpatterns = [
#     re_path(r'ws/chat/room/(?P<department>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$',consumers.ChatConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    path('ws/chat/room/<str:department>/', consumers.ChatConsumer.as_asgi())
]