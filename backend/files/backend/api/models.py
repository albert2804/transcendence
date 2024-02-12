from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

	# Already defined fields (from AbstractUser)
	# username
	# first_name
	# last_name
	# email
	# password
	# groups
	# user_permissions
	# is_staff
	# is_active
	# is_superuser
	# last_login
	# date_joined


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
	def request_friend(self, user):
		if user in self.friends.all() or user in self.friends_requests.all():
			return 0 # already friends or request already sent
		if self in user.friends_requests.all():
			self.friends.add(user)
			self.friends_requests.remove(user)
			user.friends_requests.remove(self)
			return 1 # request accepted (already sent by the other user)
		else:
			self.friends_requests.add(user)
			return 2 # request sent
	
	# remove a friend or cancel a friend request
	def remove_friend(self, user):
		if user in self.friends_requests.all():
			self.friends_requests.remove(user)
			user.friends_requests.remove(self)
			return 1 # request canceled
		if user in self.friends.all():
			self.friends.remove(user)
			return 2 # friend removed
		return 0 # no friend or request found
