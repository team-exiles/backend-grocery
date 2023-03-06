import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Item, User, ItemList
from channels.db import database_sync_to_async
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

    @database_sync_to_async
    def get_item(self, item_id):
        return Item.objects.get(id=item_id)

    @database_sync_to_async
    def get_or_create_list(self, itemlist_id):
        return ItemList.objects.get_or_create(id=itemlist_id)

    @database_sync_to_async
    def create_item(self, list_obj, item_text):
        return Item.objects.create(list_for_items=list_obj, item=item_text)

    async def receive(self, text_data):
        data = json.loads(text_data)
        item_id = data.get('item_id')
        archived = data.get('archived')
        print(archived)

        if item_id is not None:
            item = await sync_to_async(Item.objects.get)(id=item_id)
            list_obj, _ = await sync_to_async(ItemList.objects.get_or_create)(id=self.itemlist_id)

            # Add the item to the list and save it
            new_item = await self.create_item(list_obj, item.item)

            # Save the new item to the database
            await self.save_item(new_item)

        if archived is not None:
            print("HELLO!!!!!!!!!!!!!!")
            list_obj = await self.update_list(self.itemlist_id, archived)
            # Send the updated archived status to the client
            await self.save_list(list_obj)

            # Send a message to the list group with the updated list
            await self.channel_layer.group_send(
                self.itemlist_group_name,
                {
                    'type': 'list.update',
                    'list': await self.list_to_json(list_obj),
                }
            )

    @database_sync_to_async
    def save_item(self, item):
        item.save()

    @database_sync_to_async
    def save_list(self, list_obj):
        list_obj.save()

    @database_sync_to_async
    def update_list(self, itemlist_id, archived):
        itemlist, _ = ItemList.objects.get_or_create(id=itemlist_id)
        itemlist.archived = archived
        itemlist.save()
        return itemlist

    @database_sync_to_async
    def list_to_json(self, list_obj):
        return list_obj.to_json()
    
    # async def archived_update(self, event):
    #     # Update the archived field of the list
    #     itemlist_id = event['itemlist_id']
    #     archived = event['archived']
    #     await self.update_list(itemlist_id, archived)

    #     # Send the updated archived status to the client
    #     await self.send(text_data=json.dumps({
    #         'archived': archived
    #     }))

    async def list_update(self, event):
        # Send the updated list to the client
        await self.send(text_data=json.dumps(event['list']))