from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # Calls on the ChatConsumer class.
    re_path(r'ws/lists/(?P<itemlist_id>\w+)/$', consumers.ListConsumer.as_asgi()),
]

# ws/list/(?P<int:itemlist_id>\w+)/$