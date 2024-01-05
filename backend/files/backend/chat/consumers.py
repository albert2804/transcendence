from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
import json

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.chat_online = status
        user.save()

    @database_sync_to_async
    def get_registered_users(self):
        User = get_user_model()
        return list(User.objects.all())

    @database_sync_to_async
    def save_message(self, sender, receiver_id, message):
        from .models import ChatMessage
        User = get_user_model()
        receiver = User.objects.get(id=int(receiver_id))
        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

    # get all saved messages for the user (sent and received) from the database
    @database_sync_to_async
    def get_saved_messages(self, user):
        from .models import ChatMessage
        messages = list(ChatMessage.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).order_by('created_at'))
        return messages
    
    @database_sync_to_async
    def update_unread_messages(self, user, chat_id):
        from .models import ChatMessage
        ChatMessage.objects.filter(
            sender__id=int(chat_id), receiver=user
        ).update(unread=False)


    # get messages from database and send them to the user
    async def send_saved_messages(self, user):
        messages = await self.get_saved_messages(user)
        for message in messages:
            sender_id = str(await database_sync_to_async(lambda: message.sender.id)())
            chat_id = str(await database_sync_to_async(lambda: message.receiver.id if sender_id == self.scope["user"].id.__str__() else sender_id)())
            unread = not (sender_id == self.scope["user"].id.__str__()) and message.unread
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message.message,
                'sender_id': sender_id,
                'receiver_id': self.scope["user"].id.__str__(),
                'chat_id': chat_id,
                'unread': unread
            }))

    async def connect(self):
        await self.accept()
        if self.scope["user"].is_authenticated:
            # add user to his own group / create group for the user
            await self.channel_layer.group_add(
                f"chat_{self.scope['user'].id}",
                self.channel_name
            )
            # add user to chat group (general group to update user list etc.)
            await self.channel_layer.group_add(
                "chat",
                self.channel_name
            )
            # update user status
            await self.update_user_status(self.scope["user"], True)
            # send new user list to all users
            await self.channel_layer.group_send("chat",{'type': 'user_list',})
            # send saved messages to user
            await self.send_saved_messages(self.scope["user"])

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                f"chat_{self.scope['user'].id}",
                self.channel_name
            )
        await self.update_user_status(self.scope["user"], False)
        await self.channel_layer.group_send("chat",{'type': 'user_list',})

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            if (text_data_json.get('type') == 'message'):
                message = text_data_json.get('message')
                receiver = text_data_json.get('receiver_id')
                if message and receiver:
                    await self.save_message(self.scope["user"], receiver, message)
                    # send message to the sender itself
                    await self.channel_layer.group_send(
                        f"chat_{self.scope['user'].id}",
                        {
                            'type': 'chat_message',
                            'message': message,
                            'sender_id': self.scope["user"].id.__str__(),
                            'chat_id': receiver,
                            'unread' : False,
                        }
                    )
                    # send message to the receivers group
                    await self.channel_layer.group_send(
                        f"chat_{receiver}",
                        {
                            'type': 'chat_message',
                            'message': message,
                            'sender_id': self.scope["user"].id.__str__(),
                            'chat_id': self.scope["user"].id.__str__(),
                            'unread' : True,
                        }
                    )
            elif (text_data_json.get('type') == 'read_info'):
                chat_id = text_data_json.get('chat_id')
                if chat_id:
                    # set all messages from the sender to read
                    await self.update_unread_messages(self.scope["user"], chat_id)
                    print(f"set all messages from {chat_id} to read")
        except json.JSONDecodeError:
            print(f"Ungültiges JSON erhalten: {text_data}")
    
    
    # group message handlers:
            
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': self.scope["user"].id.__str__(),
            'chat_id': event['chat_id'],
            'unread': event['unread'],
        }))
    
    async def user_list(self, event):
        reg_users = await self.get_registered_users()
        users = [{'username': user.username, 'id': user.id, 'chat_online': user.chat_online} for user in reg_users]
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users,
            'own_id': self.scope["user"].id.__str__(),
        }))
