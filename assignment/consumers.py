import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import localtime

from .models import Assignment, Comment


class CommentConsumer(WebsocketConsumer):

    def connect(self):
        self.assignment_uuid = self.scope['url_route']['kwargs']['assignment_uuid']
        self.room_name = f'{self.assignment_uuid}_comments'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if not self.scope['user'].is_authenticated:
            return
        text_data = json.loads(text_data)
        comment = Comment.objects.create(
            content=text_data['content'],
            created_by=self.scope['user'],
            assignment=Assignment.objects.get(uuid=self.assignment_uuid)
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'comment.send',
                'content': comment.content,
                'created_by': comment.created_by.username,
                'created_at': localtime(comment.created_at).strftime('%d %b %Y %H:%M')
            }
        )

    def comment_send(self, event):
        self.send(json.dumps({
            'content': event['content'],
            'created_by': event['created_by'],
            'created_at': event['created_at']
        }))
