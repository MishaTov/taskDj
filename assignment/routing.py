from django.urls import path
from .consumers import CommentConsumer


websocket_urlpatterns = [
    path('assignment/<uuid:assignment_uuid>/', CommentConsumer.as_asgi()),
]
