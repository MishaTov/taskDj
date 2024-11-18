import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import localtime

from .models import Assignment, Comment


def post_comment(data, user, assignment_uuid):
    comment = Comment.objects.create(
        content=data['content'],
        created_by=user,
        assignment=Assignment.objects.get(uuid=assignment_uuid)
    )
    return {
        'uuid': str(comment.uuid),
        'content': comment.content,
        'created_by': comment.created_by.username,
        'created_at': localtime(comment.created_at).strftime('%d %b %Y %H:%M')
    }


def edit_comment(data):
    comment = Comment.objects.get(uuid=data['uuid'])
    comment.content = data['content']
    if not comment.is_edited:
        comment.is_edited = True
    comment.save(update_fields=['content', 'is_edited'])
    return {
        'uuid': str(comment.uuid),
        'content': comment.content,
    }


def delete_comment(data):
    comment = Comment.objects.get(uuid=data['uuid'])
    comment.delete()
    return {
        'uuid': data['uuid'],
    }


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
        data = {'type': text_data['event']}
        if text_data['event'] == 'comment.post':
            data.update(
                post_comment(text_data, self.scope['user'], self.assignment_uuid)
            )
        elif text_data['event'] == 'comment.edit':
            try:
                data.update(
                    edit_comment(text_data)
                )
            except Comment.DoesNotExist:
                return
        elif text_data['event'] == 'comment.delete':
            try:
                data.update(
                    delete_comment(text_data)
                )
            except Comment.DoesNotExist:
                return
        async_to_sync(self.channel_layer.group_send)(self.room_name, data)

    def comment_post(self, event):
        self.send(json.dumps({
            'event': event['type'],
            'uuid': event['uuid'],
            'content': event['content'],
            'created_by': event['created_by'],
            'created_at': event['created_at']
        }))

    def comment_edit(self, event):
        self.send(json.dumps({
            'event': event['type'],
            'uuid': event['uuid'],
            'content': event['content'],
        }))

    def comment_delete(self, event):
        self.send(json.dumps({
            'event': event['type'],
            'uuid': event['uuid'],
        }))
