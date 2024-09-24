import json
from channels.generic.websocket import AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # تحديد اسم الغرفة من عنوان URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # الانضمام إلى مجموعة الغرفة باستخدام group_add
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة المجموعة عند قطع الاتصال
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # استقبال الرسائل عبر WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # إرسال الرسالة إلى مجموعة الغرفة
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # معالجة الرسالة المرسلة وإرسالها إلى WebSocket
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatGroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
