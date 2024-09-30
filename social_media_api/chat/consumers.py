import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageGroup, GroupsManage, GroupMembership



class ChatGroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        user = self.scope["user"]
        if user.is_authenticated:
            
            try:
                # Check if the group exists
                self.group = await database_sync_to_async(GroupMembership.objects.get)(groupID=self.room_name)
                
                # Check if the user is a member of the group
                # membership = await database_sync_to_async(GroupMembership.objects.get)(user=user, group=self.group)

                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()

            except GroupsManage.DoesNotExist:
                await self.close()

            except GroupMembership.DoesNotExist:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        sender = self.scope["user"]

        # Save the message to the database (async call)
        await self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message},
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, sender, message):
        # Save the message in the MessageGroup model
        return MessageGroup.objects.create(
            group=self.group,
            sender=sender,
            content=message
        )