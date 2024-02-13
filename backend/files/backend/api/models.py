from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.consumers import ChatConsumer
from datetime import datetime
from asgiref.sync import sync_to_async

class CustomUser(AbstractUser):
	# Custom fields
	chat_online = models.BooleanField(default=False)
	profile_pic = models.FileField(upload_to='profilepic', default='profilepic/default.jpeg', blank=True, null=True)
	alias = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alias')
	friends = models.ManyToManyField('self', blank=True)
	friends_requests = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='friend_requests_received')
	blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocked_by_users')
	is_42_login = models.BooleanField(default=False)
	num_games_played = models.IntegerField(default=0)
	num_games_won = models.IntegerField(default=0)
	
	# mobile = models.CharField(max_length=20, blank=True, null=True)
	def __str__(self):
		return self.username

	# this should be used to add a friend or to accept a friend request
	# so an information about the request is sent to both users chat
	async def request_friend(self, user):
		consumer = ChatConsumer()
		friends = await sync_to_async(list)(self.friends.all())
		friends_requests = await sync_to_async(list)(self.friends_requests.all())
		user_friends_requests = await sync_to_async(list)(user.friends_requests.all())
		if user in friends or user in friends_requests:
			# already friends or request already sent
			await consumer.save_and_send_message(user, self, 'You are already friends or a request has already been sent.', datetime.now(), 'info')
			return 0
		if self in user_friends_requests:
			# request accepted (already sent by the other user)
			await sync_to_async(self.friends.add)(user)
			await sync_to_async(self.friends_requests.remove)(user)
			await sync_to_async(user.friends_requests.remove)(self)
			# send info message to both users
			await consumer.save_and_send_message(self, user, 'You are now friends.', datetime.now(), 'info')
			await consumer.save_and_send_message(user, self, 'You are now friends.', datetime.now(), 'info')
			# update the user_list of both users (who is online...)
			await consumer.update_user_list(self)
			await consumer.update_user_list(user)
			return 1 
		else:
			# request sent
			await sync_to_async(self.friends_requests.add)(user)
			await consumer.save_and_send_message(user, self, 'Friend request sent.', datetime.now(), 'info')
			await consumer.save_and_send_message(self, user, 'Friend request received.', datetime.now(), 'info')
			return 2 

	# remove a friend or cancel a friend request
	async def remove_friend(self, user):
		consumer = ChatConsumer()
		friends = await sync_to_async(list)(self.friends.all())
		friends_requests = await sync_to_async(list)(self.friends_requests.all())
		user_friends_requests = await sync_to_async(list)(user.friends_requests.all())
		if user in friends_requests or self in user_friends_requests:
			# request canceled
			await sync_to_async(self.friends_requests.remove)(user)
			await sync_to_async(user.friends_requests.remove)(self)
			await consumer.save_and_send_message(user, self, 'Friend request canceled.', datetime.now(), 'info')
			await consumer.save_and_send_message(self, user, 'Friend request canceled.', datetime.now(), 'info')
			return 1
		if user in friends:
			# friend removed
			await sync_to_async(self.friends.remove)(user)
			await consumer.save_and_send_message(user, self, 'You are no longer friends.', datetime.now(), 'info')
			await consumer.save_and_send_message(self, user, 'You are no longer friends.', datetime.now(), 'info')
			# update user list
			await consumer.update_user_list(self)
			await consumer.update_user_list(user)
			return 2
		# no friend or request found
		await consumer.save_and_send_message(user, self, "You are not friends and have no friend requests.", datetime.now(), 'info')
		return 0
