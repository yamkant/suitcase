import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from products.constants import ProductUploadedStatusEnum

def sync_function(username):
    from products.models import Product
    prodQs = Product.objects.filter(
        user_id__username=username,
        is_uploaded=ProductUploadedStatusEnum.NEED_ALARM.value
    )
    prod_list = [
        {
            "prod_id": prodQ.id,
            "date": prodQ.created_at.strftime("%Y-%m-%d %H:%M"),
        } for prodQ in prodQs
    ]
    return prod_list

async_function = sync_to_async(sync_function, thread_sensitive=True)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # if message = 
        if message == "check_product_upload_status":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']

        username = self.room_group_name[5:]
        result = await async_function(username)

        await self.send(text_data=json.dumps({
            'type': 'uploaded',
            'data': result
        }))
