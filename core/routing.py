from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # Calls on the ChatConsumer class.
    re_path(r'ws/list/(?P<itemlist_id>\w+)/$', consumers.ListConsumer.as_asgi()),
]