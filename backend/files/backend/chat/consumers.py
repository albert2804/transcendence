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

    async def save_and_send_message(self, sender, receiver , message, date, subtype='msg'):
        from .models import ChatMessage
        User = get_user_model()
        await database_sync_to_async(lambda: ChatMessage.objects.create(sender=sender, receiver=receiver, message=message, created_at=date, subtype=subtype))()
        # if the subtype is 'info', do not send the message to the sender
        if subtype != 'info':
            await self.channel_layer.group_send(
                f"chat_{self.scope['user'].id}",
                    {
                        'type': 'chat_message',
                        'message': message,
                        'subtype': subtype,
                        'sender_id': sender.id.__str__(),
                        'chat_id': receiver.id.__str__(),
                        'unread' : False,
                        'date': date.strftime("%H:%M"),
                    })
        # send message to the receivers group
        await self.channel_layer.group_send(
            f"chat_{receiver.id}",
            {
                'type': 'chat_message',
                'message': message,
                'subtype': subtype,
                'sender_id': sender.id.__str__(),
                'chat_id': sender.id.__str__(),
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
            subtype = str(await database_sync_to_async(lambda: message.subtype)())
            # check if message is from today (only send time if it is from today)
            local_created_at = message.created_at.astimezone(timezone('Europe/Berlin'))
            if local_created_at.date() == current_date:
                date_format = "%H:%M"
            else:
                date_format = "%d.%m.%Y %H:%M"
            # do not send message if subtype is 'info' and the sender is the user itself
            if subtype == 'info' and sender_id == self.scope["user"].id.__str__():
                continue
            # send message to the user
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message.message,
                'subtype': subtype,
                'sender_id': sender_id,
                'receiver_id': self.scope["user"].id.__str__(),
                'chat_id': chat_id,
                'unread': unread,
                'date': local_created_at.strftime(date_format),
            }))
    
    async def handle_block_command(self, text_data):
        blocked_user_id = text_data.get('receiver_id')
        if blocked_user_id:
            blocked_user = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(blocked_user_id)))()
            if blocked_user:
                # check if already blocked
                if await database_sync_to_async(lambda: self.scope['user'].blocked_users.filter(id=blocked_user_id).exists())():
                    await self.save_and_send_message(blocked_user, self.scope["user"], "This user is already blocked.", datetime.now(), 'info')
                else:
                    # add blocked user to the senders block list
                    await database_sync_to_async(lambda: self.scope['user'].blocked_users.add(blocked_user))()
                    await self.save_and_send_message(blocked_user, self.scope["user"], "You blocked this user.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], blocked_user, "You are blocked by this user.", datetime.now(), 'info')
    
    async def handle_unblock_command(self, text_data):
        blocked_user_id = text_data.get('receiver_id')
        if blocked_user_id:
            blocked_user = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(blocked_user_id)))()
            if blocked_user:
                if not await database_sync_to_async(lambda: self.scope['user'].blocked_users.filter(id=blocked_user_id).exists())():
                    await self.save_and_send_message(blocked_user, self.scope["user"], "This user is not blocked.", datetime.now(), 'info')
                else:
                    await database_sync_to_async(lambda: self.scope['user'].blocked_users.remove(blocked_user))()
                    await self.save_and_send_message(blocked_user, self.scope["user"], "You unblocked this user.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], blocked_user, "You are unblocked by this user.", datetime.now(), 'info')
    
    async def handle_friend_command(self, text_data):
        receiver_id = text_data.get('receiver_id')
        if receiver_id:
            receiver = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(receiver_id)))()
            if receiver:
                result = await database_sync_to_async(lambda: self.scope['user'].request_friend(receiver))()
                if result == 0:
                    await self.save_and_send_message(receiver, self.scope["user"], "You are already friends or you already requested this user.", datetime.now(), 'info')
                elif result == 1:
                    await self.save_and_send_message(receiver, self.scope["user"], "You are now friends.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], receiver, "You are now friends.", datetime.now(), 'info')
                elif result == 2:
                    await self.save_and_send_message(receiver, self.scope["user"], "Friend request sent.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], receiver, "Friend request received.", datetime.now(), 'info')

    async def handle_unfriend_command(self, text_data):
        receiver_id = text_data.get('receiver_id')
        if receiver_id:
            receiver = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(receiver_id)))()
            if receiver:
                result = await database_sync_to_async(lambda: self.scope['user'].remove_friend(receiver))()
                if result == 0:
                    await self.save_and_send_message(receiver, self.scope["user"], "You are not friends and have no friend requests.", datetime.now(), 'info')
                elif result == 1:
                    await self.save_and_send_message(receiver, self.scope["user"], "Friend request canceled.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], receiver, "Friend request canceled.", datetime.now(), 'info')
                elif result == 2:
                    await self.save_and_send_message(receiver, self.scope["user"], "Friend removed.", datetime.now(), 'info')
                    await self.save_and_send_message(self.scope["user"], receiver, "Friend removed.", datetime.now(), 'info')

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
            # check for command type
            if (text_data_json.get('type') == 'command'):
                command = text_data_json.get('command')
                if command == '/block':
                    await self.handle_block_command(text_data_json)
                elif command == '/unblock':
                    await self.handle_unblock_command(text_data_json)
                elif command == '/friend':
                    await self.handle_friend_command(text_data_json)
                elif command == '/unfriend':
                    await self.handle_unfriend_command(text_data_json)
            elif (text_data_json.get('type') == 'message'):
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
                            await self.save_and_send_message(receiver_user, self.scope["user"], "You are blocked by this user.", datetime.now(), 'info')
                            return
                        else:
                            # save and send message
                            receiver = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(receiver_id)))()
                            if receiver:
                                await self.save_and_send_message(self.scope["user"], receiver, message, date)
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
