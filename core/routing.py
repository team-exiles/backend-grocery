from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # Calls on the ChatConsumer class.
    re_path(r"ws/lists/<int:list_id>/$", consumers.ListConsumer.as_asgi()),
    re_path(r"ws/lists/$", consumers.ListConsumer.as_asgi()),
]