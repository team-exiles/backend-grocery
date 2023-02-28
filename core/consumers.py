import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from .models import Item, User, ItemList
# from .serializers import MessageSerializer


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