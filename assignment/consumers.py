from channels.generic.websocket import WebsocketConsumer


class CommentConsumer(WebsocketConsumer):

    def connect(self):
        super().connect()

    def receive(self, text_data=None, bytes_data=None):
        pass
