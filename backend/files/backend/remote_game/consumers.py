from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .player import Player
from .gameHandler import GameHandler
from django.apps import apps
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

class RemoteGameConsumer(AsyncWebsocketConsumer):
	# all instances of RemoteGameConsumer
	all_consumer_groups = []

	# list of players in the waiting group for unranked games (mixed room for guests and registered users)
	training_waiting_room = []
	# list of players in the waiting group for ranked games (only registered users)
	ranked_waiting_room = []

	# async def fast_game(self, event): # NOT USED BUT INTERESTING (UNRANKED GAME)
	# 	print("fast_game called")
	# 	user_id_1 = event['user_id_1']
	# 	user_id_2 = event['user_id_2']
	# 	user_1 = await sync_to_async(get_user_model().objects.get)(id=user_id_1)
	# 	user_2 = await sync_to_async(get_user_model().objects.get)(id=user_id_2)
	# 	player1 = Player.get_player_by_user(user_1)
	# 	player2 = Player.get_player_by_user(user_2)
	# 	if player1 == None or player2 == None:
	# 		print("Error: player not found")
	# 		return
	# 	game_group = await GameHandler.create(player1, player2)
	# 	# open the game modal for both players
	# 	await self.channel_layer.group_send(
	# 		f"game_{player1.get_user().id}_{player2.get_user().id}",
	# 		{
	# 			'type': 'open_game_modal',
	# 		})
	# 	await player1.send_state()
	# 	await player2.send_state()
	# 	asyncio.ensure_future(game_group.start_game())


	# Invites a user to a game (ranked)
	# Same as sending /play request to a user in the chat
	# 
	# async_to_sync(channel_layer.group_send)('gameconsumer_' + str(request.user.id), {
	# 	'type': 'invite_to_game',
	# 	'user_id_1': request.user.id,
	# 	'user_id_2': receiver.id,
	# })
	async def invite_to_game(self, event):
		print("invite_to_game called")
		user_id_1 = event['user_id_1']
		user_id_2 = event['user_id_2']
		user_1 = await sync_to_async(get_user_model().objects.get)(id=user_id_1)
		user_2 = await sync_to_async(get_user_model().objects.get)(id=user_id_2)
		if user_1 == None or user_2 == None:
			print("Error: user not found")
			return
		await user_1.invite_to_game(user_2)
	
	# Starts a tournament game between two users.
	# You have to send the user ids and the db_game id (RemoteGame object) as event data.
	# 
	# async_to_sync(channel_layer.group_send)('gameconsumer_' + str(request.user.id), {
	# 	'type': 'start_tournament_game',
	# 	'user_1_id': user_1.id,
	# 	'user_2_id': user_2.id,
	# 	'db_game_id': db_game.id,
	#		'tour_id
	# })
	async def start_tournament_game(self, event):
		user_1_id = event.get('user_id_1')
		user_2_id = event.get('user_id_2')
		db_game_id = event.get('db_game_id')
		tour_id = event.get('tour_id')
		if user_1_id and user_2_id and db_game_id and tour_id:
			user_1 = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(user_1_id)))()
			user_2 = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(user_2_id)))()
			RemoteGame = apps.get_model('remote_game', 'RemoteGame')
			db_game = await database_sync_to_async(lambda: RemoteGame.objects.get(id=int(db_game_id)))()
			Tournament = apps.get_model('tournament', 'Tournament')
			db_tour = await database_sync_to_async(lambda: Tournament.objects.get(id=int(tour_id)))()
			if user_1 and user_2 and db_game and db_tour:
				player_1 = Player.get_player_by_user(user_1)
				player_2 = Player.get_player_by_user(user_2)
				if player_1 == None or player_2 == None:
					return
				game_group = await GameHandler.create(player_1, player_2, ranked=True, db_entry=db_game, tournament=db_tour)
				await game_group.channel_layer.group_send(
					game_group.game_group,
					{
						'type': 'open_game_modal',
					})
				asyncio.create_task(game_group.start_game())

	# Tries to create a guest player with the given alias
	# If the alias is already taken or empty, the player gets an "alias_exists" message
	async def create_guest_player(self, alias):
		if alias == "":
			await self.send(text_data=json.dumps({
				'type': 'alias_exists',
			}))
			return
		for p in Player.all_players:
			if p.alias == alias:
				await self.send(text_data=json.dumps({
					'type': 'alias_exists',
				}))
				return
		from api.models import CustomUser
		exists = await sync_to_async(CustomUser.objects.filter(alias=alias).exists)()
		if exists:
			await self.send(text_data=json.dumps({
				'type': 'alias_exists',
			}))
			return
		self.scope["user"].alias = alias
		player = Player(self.scope["user"], self.channel_name)
		# player.alias = alias
		await player.send_state()
		print(f"Anonymous user upgraded to guest player with alias {alias}.")

	# Adds the player to the waiting room list (for unranked games)
	async def add_to_training_waiting_room(self, player):
		if len(RemoteGameConsumer.training_waiting_room) >= 1:
			player1 = RemoteGameConsumer.training_waiting_room[0]
			RemoteGameConsumer.training_waiting_room.pop(0)
			game_group = await GameHandler.create(player1, player)
			asyncio.create_task(game_group.start_game())
		else:
			RemoteGameConsumer.training_waiting_room.append(player)
		await player.send_state()
	
	# Adds the player to the waiting room list (for ranked games)
	async def add_to_ranked_waiting_room(self, player):
		if player.get_user().is_authenticated:
			if len(RemoteGameConsumer.ranked_waiting_room) >= 1:
				player1 = RemoteGameConsumer.ranked_waiting_room[0]
				RemoteGameConsumer.ranked_waiting_room.pop(0)
				game_group = await GameHandler.create(player1, player, ranked=True)
				asyncio.create_task(game_group.start_game())
			else:
				RemoteGameConsumer.ranked_waiting_room.append(player)
			await player.send_state()
	
	# This function is called when a new connection is established
	# Checks if user is authenticated or not
	# If authenticated, checks if user is already connected with another device
	async def connect(self):
		await self.accept()
		if self.scope["user"].is_authenticated:
			await self.channel_layer.group_add(f"gameconsumer_{self.scope['user'].id}", self.channel_name)
			if "gameconsumer_" + str(self.scope['user'].id) not in RemoteGameConsumer.all_consumer_groups:
				RemoteGameConsumer.all_consumer_groups.append("gameconsumer_" + str(self.scope['user'].id))
			if Player.get_channel_by_user(self.scope["user"]) != None:
				await self.send(text_data=json.dumps({
					'type': 'redirect',
					'page': "other_device",
				}))
				print(f"User {self.scope['user'].id} connected to game-websocket with another device.")
				return
			player = Player(self.scope["user"], self.channel_name)
			await player.send_state()
			print(f"{self.scope['user'].alias} connected to game-websocket.")
		else:
			print(f"Anonymous user connected to game-websocket.")
			await self.send(text_data=json.dumps({
				'type': 'redirect',
				'page': "alias_screen",
			}))
	
	# Message handler for incoming messages
	async def receive(self, text_data):
		try:
			data = json.loads(text_data)
			player = Player.get_player_by_channel(self.channel_name)
			if player == None:
				if self.scope["user"].is_authenticated:
					if data.get('type') == 'change_device':
						if Player.get_channel_by_user(self.scope["user"]) != None:
							oldchannel = Player.get_channel_by_user(self.scope["user"])
							player = Player.get_player_by_channel(oldchannel)
							await player.change_channel(self.channel_name)
				else:
					if data.get('type') == 'create_guest_player':
						await self.create_guest_player(data.get('alias'))
			else:
				# general message handling for connected players
				if data.get('type') == 'slow_device':
					player.fps = 12 # (worked with 12fps on esp8266)
				elif data.get('type') == 'back_to_menu':
					if player.get_game_handler() != None:
						player.get_game_handler().give_up(player)
					if player in RemoteGameConsumer.training_waiting_room:
						RemoteGameConsumer.training_waiting_room.remove(player)
					if player in RemoteGameConsumer.ranked_waiting_room:
						RemoteGameConsumer.ranked_waiting_room.remove(player)
					await player.send_state()
				elif data.get('type') == 'create_guest_player_2':
					if data.get('alias') == "":
						await self.send(text_data=json.dumps({
							'type': 'alias_exists',
						}))
						return
					player.alias_2 = data.get('alias')
					# start local game after both players have chosen an alias
					if player.get_game_handler() == None and player.alias_2 != None:
						game_group = await GameHandler.create(player, player)
						asyncio.create_task(game_group.start_game())
					else:
						await player.send_state()
				elif data.get('type') == "give_up":
					if player.get_game_handler() != None:
						player.get_game_handler().give_up(player)
					if player in RemoteGameConsumer.training_waiting_room:
						RemoteGameConsumer.training_waiting_room.remove(player)
					if player in RemoteGameConsumer.ranked_waiting_room:
						RemoteGameConsumer.ranked_waiting_room.remove(player)
					await player.send_state()
				# message handling for players in a game
				if player.get_game_handler() != None:
					if (data.get('type') == 'key_pressed' or data.get('type') == 'key_released'):
						player.get_game_handler().update_paddle(player, data.get('key'), data.get('type'))

				# message handling for players in the menu
				else:
					if data.get('type') == 'start_training_game':
						await self.add_to_training_waiting_room(player)
					elif data.get('type') == 'start_ranked_game':
						await self.add_to_ranked_waiting_room(player)
					elif data.get('type') == 'start_local_game':
						if (player.alias_2 != None):
							game_group = await GameHandler.create(player, player)
							asyncio.create_task(game_group.start_game())
						else:
							await self.send(text_data=json.dumps({
								'type': 'redirect',
								'page': "alias_screen_2",
							}))
		except json.JSONDecodeError:
			print(f"Error handling received message from a game-websocket: {text_data}")
	
	# This function is called when the connection is closed
	# Removes the player from game and waiting room and deletes the player object
	async def disconnect(self, close_code):
		if self.scope["user"].is_authenticated:
			# send close modal message to client
			await self.channel_layer.group_send(f"gameconsumer_{self.scope['user'].id}",{'type': 'close_game_modal',})
			await self.channel_layer.group_discard(f"gameconsumer_{self.scope['user'].id}", self.channel_name)
			if "gameconsumer_" + str(self.scope['user'].id) in RemoteGameConsumer.all_consumer_groups:
				RemoteGameConsumer.all_consumer_groups.remove("gameconsumer_" + str(self.scope['user'].id))
		player = Player.get_player_by_channel(self.channel_name)
		if player != None:
			# give up if the user is in a game
			if player.get_game_handler() != None:
				player.get_game_handler().give_up(player)
			if player in RemoteGameConsumer.training_waiting_room:
				RemoteGameConsumer.training_waiting_room.remove(player)
			if player in RemoteGameConsumer.ranked_waiting_room:
				RemoteGameConsumer.ranked_waiting_room.remove(player)
			Player.all_players.remove(Player.get_player_by_channel(self.channel_name))
			print(f"{self.scope['user'].alias} disconnected from game-websocket.")

	# API-Function for paddle movement (only used for the api)
	async def move_paddle(self, event):
		direction = event.get('direction')
		player = Player.get_player_by_channel(self.channel_name)
		if player.game_handler != None:
			game_handler = GameHandler.get_game_handler_by_name(player.game_handler)
			if game_handler == None:
				return
			if direction == "up" or direction == "UP":
				game_handler.update_paddle(player, "ArrowUp", "key_pressed")
			elif direction == "down" or direction == "DOWN":
				game_handler.update_paddle(player, "ArrowDown", "key_pressed")
			else:
				game_handler.update_paddle(player, "ArrowUp", "key_released")
				game_handler.update_paddle(player, "ArrowDown", "key_released")
		

	#####################
	## MESSAGE HANDLER ##
	#####################
	
	# This message is used to redirect the players to the different pages of the pong game
	# "playing"				--> screen for playing the game
	# "waiting" 			--> show a waiting message
	# "menu" 				--> show the menu
	# "other_device" 		--> show a message that the user is already connected with another device (ask for change device)
	# "alias_screen" 		--> let the user choose an alias (for guest players)
	async def redirect(self, event):
		await self.send(text_data=json.dumps({
			'type': 'redirect',
			'page': event['page'], 
		}))
	
	# This message is used to update the player names!
	# It will be sent to the players before the game starts
	async def player_names(self, event):
		await self.send(text_data=json.dumps({
			'type': 'player_names',
			'p1_name': event['p1_name'],
			'p2_name': event['p2_name'],
		}))
	
	# This message is used to update the game state (ball, paddles, score, etc.)
	# The players needs to be in the "playing" page to receive this message
	async def game_update(self, event):
		await self.send(text_data=json.dumps({
			'type': 'game_update',
			'state': event['state'],
			'high_score': event['high_score'],
		}))

	# This message is used to inform the players about the result of the game
	# The result can be "winner", "loser" or "tied"
	# For local games, the result can be "tied", "left" or "right"
	async def game_result(self, event):
		await self.send(text_data=json.dumps({
			'type': 'game_result',
			'result': event['result'],
		}))

	# This message is used to inform a guest player that the alias he chose already exists
	# the guest player needs to choose another alias
	async def alias_exists(self, event):
		await self.send(text_data=json.dumps({
			'type': 'alias_exists',
		}))

	# This message is used to open the modal in the clients browser
	async def open_game_modal(self, event):
		await self.send(text_data=json.dumps({
			'type': 'open_game_modal',
		}))

	# This message is used to close the modal in the clients browser
	async def close_game_modal(self, event):
		await self.send(text_data=json.dumps({
			'type': 'close_game_modal',
		}))