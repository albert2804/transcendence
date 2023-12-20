from channels.generic.websocket import AsyncWebsocketConsumer
import json
import random

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.my_channel_name = self.channel_name
        await self.accept()
        await self.channel_layer.group_add("chat", self.channel_name)
        # check if user is authenticated
        if self.scope["user"].is_authenticated:
            # send welcome message
            user = self.scope["user"].username
            await self.send(text_data=json.dumps({
                'message': 'Welcome to the chat, ' + user + '!',
                'sender_id': '1'
            }))
        else:
            # send error message
            await self.send(text_data=json.dumps({
                'message': 'You are not logged in.',
                'sender_id': '1'
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

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
                    }
                )
        except json.JSONDecodeError:
            print(f"Ungültiges JSON erhalten: {text_data}")

    async def chat_message(self, event):
        message = event['message']
        sender_channel_name = event['sender_channel_name']
        sender_id = 0 if sender_channel_name == self.channel_name else random.randint(1, 100)

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id.__str__()
        }))