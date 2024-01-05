# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# import json
# import random

# class ChatConsumer(AsyncWebsocketConsumer):

#     @database_sync_to_async
#     def update_user_status(self, user, status):
#         user.chat_online = status
#         user.save()
    
#     @database_sync_to_async
#     def get_registered_users(self):
#         User = get_user_model()
#         return list(User.objects.all())

#     async def connect(self):
#         self.my_channel_name = self.channel_name
#         await self.accept()
#         await self.channel_layer.group_add("chat", self.channel_name)
#         # check if user is authenticated
#         if self.scope["user"].is_authenticated:
#             # update user status
#             await self.update_user_status(self.scope["user"], True)
#             # send list of registered users
#             reg_users = await self.get_registered_users()
#             users = [{'username': user.username, 'id': user.id, 'chat_online': user.chat_online} for user in reg_users]
#             await self.send(text_data=json.dumps({
#                 'type': 'user_list',
#                 'users': users,
#                 'own_id': self.scope["user"].id.__str__(),
#             }))
#         else:
#             # send error message
#             await self.send(text_data=json.dumps({
#                 'type': 'chat_message',
#                 'message': 'You are not logged in.',
#                 'sender_id': '1'
#             }))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("chat", self.channel_name)
#         # update user status
#         await self.update_user_status(self.scope["user"], False)

#     async def receive(self, text_data):
#         try:
#             text_data_json = json.loads(text_data)
#             message = text_data_json.get('message')
#             if message:
#                 await self.channel_layer.group_send(
#                     'chat',
#                     {
#                         'type': 'chat_message',
#                         'message': message,
#                         'sender_channel_name': self.channel_name,
#                         'sender_id': self.scope["user"].id,
#                     }
#                 )
#         except json.JSONDecodeError:
#             print(f"Ungültiges JSON erhalten: {text_data}")

#     async def chat_message(self, event):
#         message = event['message']
#         sender_channel_name = event['sender_channel_name']
#         # sender_id = 0 if sender_channel_name == self.channel_name else random.randint(1, 100)
#         sender_id = event['sender_id']

#         await self.send(text_data=json.dumps({
#             'type': 'chat_message',
#             'message': message,
#             'sender_id': sender_id.__str__()
#         }))


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
        ))
        return messages
    
    # check if user is online
    # @database_sync_to_async
    # def is_user_online(self, user_id):
    #     User = get_user_model()
    #     user = User.objects.get(id=int(user_id))
    #     return user.chat_online

    # get messages from database and send them to the user
    async def send_saved_messages(self, user):
        messages = await self.get_saved_messages(user)
        for message in messages:
            sender_id = str(await database_sync_to_async(lambda: message.sender.id)())
            chat_id = str(await database_sync_to_async(lambda: message.receiver.id if sender_id == self.scope["user"].id.__str__() else sender_id)())
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message.message,
                'sender_id': sender_id,
                'chat_id': chat_id,
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
                    }
                )
                # if receiver is online, send message to the receiver
                # if await self.is_user_online(receiver):
                await self.channel_layer.group_send(
                    f"chat_{receiver}",
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': self.scope["user"].id.__str__(),
                        'chat_id': self.scope["user"].id.__str__(),
                    }
                )
        except json.JSONDecodeError:
            print(f"Ungültiges JSON erhalten: {text_data}")
    
    
    # group message handlers:
            
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'chat_id': event['chat_id'],
        }))
    
    async def user_list(self, event):
        reg_users = await self.get_registered_users()
        users = [{'username': user.username, 'id': user.id, 'chat_online': user.chat_online} for user in reg_users]
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users,
            'own_id': self.scope["user"].id.__str__(),
        }))
