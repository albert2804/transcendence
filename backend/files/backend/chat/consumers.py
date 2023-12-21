from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json
import random

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.chat_online = status
        user.save()
    
    @database_sync_to_async
    def get_registered_users(self):
        User = get_user_model()
        return list(User.objects.all())

    async def connect(self):
        self.my_channel_name = self.channel_name
        await self.accept()
        await self.channel_layer.group_add("chat", self.channel_name)
        # check if user is authenticated
        if self.scope["user"].is_authenticated:
            # update user status
            await self.update_user_status(self.scope["user"], True)
            # send list of registered users
            reg_users = await self.get_registered_users()
            users = [{'username': user.username, 'id': user.id, 'chat_online': user.chat_online} for user in reg_users]
            await self.send(text_data=json.dumps({
                'type': 'user_list',
                'users': users,
                'own_id': self.scope["user"].id.__str__(),
            }))
        else:
            # send error message
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': 'You are not logged in.',
                'sender_id': '1'
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)
        # update user status
        await self.update_user_status(self.scope["user"], False)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            if message:
                await self.channel_layer.group_send(
                    'chat',
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_channel_name': self.channel_name,
                        'sender_id': self.scope["user"].id,
                    }
                )
        except json.JSONDecodeError:
            print(f"Ungültiges JSON erhalten: {text_data}")

    async def chat_message(self, event):
        message = event['message']
        sender_channel_name = event['sender_channel_name']
        # sender_id = 0 if sender_channel_name == self.channel_name else random.randint(1, 100)
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id.__str__()
        }))