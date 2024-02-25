from django.contrib.auth.models import AbstractUser
from remote_game.gameHandler import GameHandler
from remote_game.consumers import RemoteGameConsumer
from remote_game.player import Player
from django.db import models
from chat.consumers import ChatConsumer
from datetime import datetime
from asgiref.sync import sync_to_async	
from django.core.validators import FileExtensionValidator
import asyncio
import json

class CustomUser(AbstractUser):
	# Custom fields
	chat_online = models.BooleanField(default=False)
	profile_pic = models.FileField(upload_to='profilepic', default='profilepic/default.jpeg', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpeg','png'])])
	alias = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alias')
	friends = models.ManyToManyField('self', blank=True)
	friends_requests = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='friend_requests_received')
	blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocked_by_users')
	game_invites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='game_invites_received')
	is_42_login = models.BooleanField(default=False)
	num_games_played = models.IntegerField(default=0)
	num_games_won = models.IntegerField(default=0)
	mmr = models.IntegerField(default=200)
	ranking = models.IntegerField(default=0)
	date_joined = models.DateTimeField(auto_now_add=True)
	game_history = models.ManyToManyField('remote_game.RemoteGame', related_name='game_history')

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

	# invite someone to a game (ranked)
	# if the other user already invited this user, the game will be started
	async def invite_to_game(self, user):
		consumer = ChatConsumer()
		# check if the other user already invited this user
		if user in await sync_to_async(list)(self.game_invites_received.all()):
   			# check if both player object exist
      		# (player object is created when the user connects and deleted when the user disconnects)
			player1 = Player.get_player_by_user(self)
			player2 = Player.get_player_by_user(user)
			if player1 == None or player2 == None:
				await consumer.save_and_send_message(user, self, 'Player seems to be offline. Try again later.', datetime.now(), 'info')
				return
			# check if already playing
			# (a playing player has a game_handler attribute which is not None)
			if player1.game_handler != None or player2.game_handler != None:
				await consumer.save_and_send_message(user, self, 'Player is already playing. Try again later.', datetime.now(), 'info')
				return
			# remove players from the waiting rooms
   			# (to avoid multiple games running for the same players)
			game_consumer = RemoteGameConsumer()
			if player1 in game_consumer.training_waiting_room:
				game_consumer.training_waiting_room.remove(player1)
			if player1 in game_consumer.ranked_waiting_room:
				game_consumer.ranked_waiting_room.remove(player1)
			if player2 in game_consumer.training_waiting_room:
				game_consumer.training_waiting_room.remove(player2)
			if player2 in game_consumer.ranked_waiting_room:
				game_consumer.ranked_waiting_room.remove(player2)
			# send info message to both users
			await consumer.save_and_send_message(user, self, 'You accepted the game invite.', datetime.now(), 'info')
			await consumer.save_and_send_message(self, user, 'Game invite got accepted.', datetime.now(), 'info')
			# remove invites from both users
			await sync_to_async(self.game_invites.remove)(user)
			await sync_to_async(user.game_invites.remove)(self)
			# create a new game handler
			game_handler = await GameHandler.create(player1, player2, ranked=True)
			# open the game modal for both players
			await game_handler.channel_layer.group_send(
				game_handler.game_group,
				{
					'type': 'open_game_modal',
				})
			# start the game in another thread
			asyncio.ensure_future(game_handler.start_game())
			return
		# check if already invited
		if user in await sync_to_async(list)(self.game_invites.all()):
			await consumer.save_and_send_message(user, self, 'You already invited this user.', datetime.now(), 'info')
		else:
			# invite the other user
			await sync_to_async(self.game_invites.add)(user)
			await consumer.save_and_send_message(user, self, 'You sent a game invite.', datetime.now(), 'info')
			await consumer.save_and_send_message(self, user, 'You got a game invite.', datetime.now(), 'info')
  
	# remove a game invite
	# removes the incoming and outgoing game invites between this user and the other user
	async def remove_game_invite(self, user):
		consumer = ChatConsumer()
		# check if there are game invites between the users
		if self not in await sync_to_async(list)(user.game_invites.all()) and user not in await sync_to_async(list)(self.game_invites.all()):
			await consumer.save_and_send_message(user, self, 'There are no game invites between you and this user.', datetime.now(), 'info')
			return
		# remove the invites
		await sync_to_async(self.game_invites.remove)(user)
		await sync_to_async(user.game_invites.remove)(self)
		# send info message to both users
		await consumer.save_and_send_message(user, self, 'You canceled the game invite.', datetime.now(), 'info')
		await consumer.save_and_send_message(self, user, 'The game invite got canceled.', datetime.now(), 'info')

	def response_gamehistory(self):
		games = []
		for game in self.game_history.all():
			data = {
                'id': game.pk,
                'player1': game.return_all_data()['player1'],
                'player2': game.return_all_data()['player2'],
                'time': (game.finished_at - game.started_at).total_seconds(),
                'pointsP1': game.pointsP1,
                'pointsP2': game.pointsP2,
                'winner': game.return_all_data()['winner'],
                'loser': game.return_all_data()['loser'],
            }
			games.append(data)
		return games
			