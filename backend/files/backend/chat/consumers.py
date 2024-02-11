from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from pytz import timezone
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

    # @database_sync_to_async
    async def save_and_send_message(self, sender, receiver_id, message, date):
        from .models import ChatMessage
        User = get_user_model()
        # receiver = User.objects.get(id=int(receiver_id))
        receiver = await database_sync_to_async(lambda: User.objects.get(id=int(receiver_id)))()
        # ChatMessage.objects.create(sender=sender, receiver=receiver, message=message, created_at=date)
        await database_sync_to_async(lambda: ChatMessage.objects.create(sender=sender, receiver=receiver, message=message, created_at=date))()
        # send message to the senders group (to update chat history)
        await self.channel_layer.group_send(
            f"chat_{self.scope['user'].id}",
                {
                    'type': 'chat_message',
                    'message': message,
                    'subtype': 'msg',
                    'sender_id': self.scope["user"].id.__str__(),
                    'chat_id': receiver_id,
                    'unread' : False,
                    'date': date.strftime("%H:%M"),
                })
        # send message to the receivers group
        await self.channel_layer.group_send(
            f"chat_{receiver_id}",
            {
                'type': 'chat_message',
                'message': message,
                'subtype': 'msg',
                'sender_id': self.scope["user"].id.__str__(),
                'chat_id': self.scope["user"].id.__str__(),
                'unread' : True,
                'date': date.strftime("%H:%M"),
            })

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
        current_date = datetime.now().astimezone(timezone('Europe/Berlin')).date()
        for message in messages:
            sender_id = str(await database_sync_to_async(lambda: message.sender.id)())
            chat_id = str(await database_sync_to_async(lambda: message.receiver.id if sender_id == self.scope["user"].id.__str__() else sender_id)())
            unread = not (sender_id == self.scope["user"].id.__str__()) and message.unread
            # check if message is from today (only send time if it is from today)
            local_created_at = message.created_at.astimezone(timezone('Europe/Berlin'))
            if local_created_at.date() == current_date:
                date_format = "%H:%M"
            else:
                date_format = "%d.%m.%Y %H:%M"
            # send message to the user
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message.message,
                'subtype': 'msg',
                'sender_id': sender_id,
                'receiver_id': self.scope["user"].id.__str__(),
                'chat_id': chat_id,
                'unread': unread,
                'date': local_created_at.strftime(date_format),
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
                receiver_id = text_data_json.get('receiver_id')
                # date = models.DateTimeField(auto_now_add=True)
                date = datetime.now()
                if message and receiver_id:
                    # check if sender is in the receivers block list
                    receiver_user = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(receiver_id)))()
                    if receiver_user:
                        if await database_sync_to_async(lambda: receiver_user.blocked_users.filter(id=self.scope['user'].id).exists())():
                            # send info message to the sender that he is blocked by the receiver
                            await self.channel_layer.group_send(
                                f"chat_{self.scope['user'].id}",
                                {
                                    'type': 'chat_message',
                                    'message': "You are blocked by this user.",
                                    'subtype': 'info',
                                    'sender_id': self.scope["user"].id.__str__(),
                                    'chat_id': receiver_id,
                                    'unread' : False,
                                    'date': date.strftime("%H:%M"),
                                })
                            return
                        else:
                            # save and send message
                            await self.save_and_send_message(self.scope["user"], receiver_id, message, date)
            elif (text_data_json.get('type') == 'read_info'):
                chat_id = text_data_json.get('chat_id')
                if chat_id:
                    # set all messages from the sender to read
                    await self.update_unread_messages(self.scope["user"], chat_id)
        except json.JSONDecodeError:
            print(f"Ungültiges JSON erhalten: {text_data}")
    
    
    # group message handlers:
            
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'subtype': event.get('subtype'), # should be 'msg' or 'info' --- 'info' is for system messages like blocked user...
            'sender_id': event['sender_id'],
            'receiver_id': self.scope["user"].id.__str__(),
            'chat_id': event['chat_id'],
            'unread': event['unread'],
            'date': event['date'],
        }))
    
    async def user_list(self, event):
        reg_users = await self.get_registered_users()
        users = [{'username': user.username, 'id': user.id, 'chat_online': user.chat_online} for user in reg_users]
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users,
            'own_id': self.scope["user"].id.__str__(),
        }))
