import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Item, User, ItemList
from channels.db import database_sync_to_async
from django.forms.models import model_to_dict
from .encoder import ItemEncoder
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
# from .serializers import MessageSerializer

# myapp/consumers.py

# User = get_user_model()

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
        itemlist, _ = ItemList.objects.get_or_create(id=itemlist_id)
        return itemlist

    @database_sync_to_async
    def create_item(self, list_obj, item_text):
        return Item.objects.create(list_for_items=list_obj, item=item_text)

    async def receive(self, text_data):
        data = json.loads(text_data)
        item_data = data

        if item_data is not None:
            itemlist = await sync_to_async(ItemList.objects.get)(id=self.itemlist_id)
            new_item = Item(
                list_for_items = itemlist,
                item = item_data.get('item'),
                check_box = item_data.get('check_box'),
                missing = item_data.get('missing'),
            )

            try:
                await database_sync_to_async(new_item.save)()
                item_serializer = ItemSerializer(new_item)
                serialized_item = json.dumps(item_serializer.data)

                await self.channel_layer.group_send(
                    self.itemlist_group_name,
                    {
                        'type': 'item.new',
                        'item': serialized_item,
                    }
                )

            except Exception as e:
                raise Http404(str(e))

            # Save the new item to the database


            # Saves new item to database
            # await database_sync_to_async(new_item.save)()
            # item_serializer = ItemSerializer(new_item)
            # serialized_item = json.dumps(item_serializer.data)

            # await self.channel_layer.group_send(
            #     self.itemlist_group_name,
            #     {
            #         'type': 'item.new',
            #         'item': serialized_item,
            #     }
            # )

        archived = data.get('archived')
        active_shopping = data.get('active_shopping')

        if archived is not None:
            list_obj = await self.update_list(self.itemlist_id, archived)
            # Send the updated archived status to the client
            await self.save_list(list_obj)

        if active_shopping is not None:
            list_obj = await self.update_active_shopping(self.itemlist_id, active_shopping)
            await self.save_list(list_obj)

            # Send a message to the list group with the updated list
            await self.channel_layer.group_send(
                self.itemlist_group_name,
                {
                    'type': 'list.update',
                    'list': await self.list_to_json(list_obj),
                }
            )

    async def item_new(self, event):
        item = event['item']
        item_data = json.loads(item)
        item = Item(**item_data)
        await self.send(text_data=json.dumps({
            'type': 'item.new',
            'item': await self.item_to_json(item),
        }))

    @database_sync_to_async
    def item_to_json(self, item):
        return json.dumps(item, cls=ItemEncoder)

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
    def update_active_shopping(self, itemlist_id, active_shopping):
        itemlist = ItemList.objects.get(id=itemlist_id)
        itemlist.active_shopping = active_shopping
        itemlist.save()
        return itemlist
    
    @database_sync_to_async
    def item_to_json(self, item):
        return item.to_json()

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