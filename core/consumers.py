import json

from channels.generic.websocket import WebsocketConsumer


class ListConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        item = text_data_json['item', 'quantity']

        self.send(text_data=json.dumps({'item': item}))





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