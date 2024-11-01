from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class CommentConsumer(WebsocketConsumer):

    def connect(self):
        self.assignment_uuid = self.scope['url_route']['kwargs']['assignment_uuid']
        self.room_name = f'{self.assignment_uuid}_comments'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_name.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        super().receive()
        pass
