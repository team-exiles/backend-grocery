import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from .models import Item, User, ItemList
# from .serializers import MessageSerializer

# myapp/consumers.py

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Item, ItemList

class ListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.itemlist_id = self.scope['url_route']['kwargs']['itemlist_id']
        self.itemlist_group_name = 'list_%s' % self.itemlist_id

        # Join list group
        await self.channel_layer.group_add(
            self.itemlist_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave list group
        await self.channel_layer.group_discard(
            self.itemlist_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        item_id = data.get('item_id')

        if item_id is not None:
            item = await sync_to_async(Item.objects.get)(id=item_id)
            list_obj = await sync_to_async(ItemList.objects.get_or_create)(id=self.itemlist_id)
            

        # Add the item to the list and save it
            list_obj.items.add(item)
            await sync_to_async(list_obj.save)()

        # Send a message to the list group with the updated list
            await self.channel_layer.group_send(
                self.list_group_name,
                {
                    'type': 'list.update',
                    'list': list_obj.to_json()
                }
            )

    async def list_update(self, event):
        # Send the updated list to the client
        await self.send(text_data=json.dumps(event['list']))





# class ListConsumer(JsonWebsocketConsumer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         # Initializing with null values
#         self.user = None
#         self.list_name = None
#         self.item = None

#     def connect(self):
#         print("Connected!")
#         # Assigning user value from scope
#         self.user = self.scope['user']
#         if not self.user.is_authenticated:
#             return
        
#         # Accepts incoming socket
#         self.accept()
#         self.list_name = self.scope['url_route']['kwargs']['<int:list_id>']
#         # Creating item from kwarg value and storing it on the consumer
#         self.item, created = Item.objects.get_or_create(name=self.list_name)

#         # Accept connection
#         async_to_sync(self.channel_layer.group_add)(
#             self.list_name,
#             self.channel_name,
#         )

#         # !!!!!!!!!!!!!!!!!!!! Convert this to storing items !!!!!!!!!!!!!!!!!!!!
#         #Send last 50 messaged and display them
#         messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
#         self.send_json({
#             "type": "last_50_messages",
#             "messages": MessageSerializer(messages, many=True).data,
#         })
#         # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#         self.send_json(
#             {
#                 "type": "welcome_message",
#                 "message": "Hey there! You've successfully connected!",
#             }
#         )

#     def disconnect(self, code):
#         print("Disconnected!")
#         return super().disconnect(code)
    
#     def receive_json(self, content, **kwargs):
#         message_type = content["type"]
#         if message_type == "chat_message":
#             message = Message.objects.create(
#                 from_user=self.user,
#                 to_user=self.get_receiver(),
#                 content=content['message'],
#                 # conversation=self.conversation
#                 itemList=self.ItemList
#             )
#             #Echo message to everyone in group(room/list)
#             async_to_sync(self.channel_layer.group_send)(
#                 self.list_name,
#                 {
#                 "type": "chat_message_echo",
#                 "name": self.user.username,
#                 "message": MessageSerializer(message).data,
#                 }
#             )
#         return super().receive_json(content, **kwargs)

#     def chat_message_echo(self, event):
#         print(event)
#         self.send_json(event)

#     def get_receiver(self):
#         usernames = self.conversation_name.split('__')
#         for username in usernames:
#             if username != self.user.username:
#                 #This is the receiveer
#                 return User.objects.get(username=username)

#     # #Send message back to user
#     # self.send_json({
#     #     "type": "greeting_response",
#     #     "message": "How are you?",
#     # })
#     # return super().receive_json(content, **kwargs)