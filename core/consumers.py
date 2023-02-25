import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected!")
        self.list_name = self.scope['url_route']['kwargs']['<int:list_id>']
        self.list_group_name = 'list_%s' % self.list_name

        await self.channel_layer.group_add(self.list_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("Disconnected!")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive list from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        item = text_data_json['item', 'quantity']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'item_incoming', 'item': item}
        )

    # Receive list from group
    async def item_incoming(self, event):
        item = event['item']

        #Send item to WebSocket
        await self.send(text_data=json.dumps({'item': item}))





# class ListConsumer(WebsocketConsumer):
#     def connect(self):
#         # Connect to list
#         self.list_name = self.scope["url_route"]["kwargs"]["list_name"]

#     def disconnect(self, close_code):
#         # Disconnect from list
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         item = text_data_json['item']