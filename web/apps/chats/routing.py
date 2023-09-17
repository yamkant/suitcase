from django.urls import path

from chats.consummers import ChatConsumer

websocket_urlpatterns = [
    path('chats/<str:room_name>/', ChatConsumer.as_asgi()),
]