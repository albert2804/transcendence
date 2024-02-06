from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .player import Player
from .gameHandler import GameHandler
from asgiref.sync import sync_to_async


# TODO: In Frontend: if websocket connection is closed -> show message "Connection lost. Please reload the page."
#       hmm maybe send a disconnection code to the frontend and show a message there (for example if the user is already connected with another device)
#       google about close_code for the disconnect function ;)


class RemoteGameConsumer(AsyncWebsocketConsumer):

	# list of players in the waiting group for unranked games (mixed room for guests and registered users)
	training_waiting_room = []
	# list of players in the waiting group for ranked games (only registered users)
	ranked_waiting_room = []

	# Tries to create a guest player with the given alias
	# If the alias is already taken or empty, the player gets an "alias_exists" message
	async def create_guest_player(self, alias):
		if alias == "":
			await self.send(text_data=json.dumps({
				'type': 'alias_exists',
			}))
			return
		for p in Player.all_players:
			if p.get_user().username == alias:
				await self.send(text_data=json.dumps({
					'type': 'alias_exists',
				}))
				return
		from api.models import CustomUser
		exists = await sync_to_async(CustomUser.objects.filter(username=alias).exists)()
		if exists:
			await self.send(text_data=json.dumps({
				'type': 'alias_exists',
			}))
			return
		player = Player(self.scope["user"], self.channel_name)
		player.get_user().username = alias
		await player.send_state()
		print(f"Anonymous user upgraded to guest player with alias {alias}.")

	# Adds the player to the waiting room list (for unranked games)
	async def add_to_training_waiting_room(self, player):
		if len(RemoteGameConsumer.training_waiting_room) >= 1:
			player1 = RemoteGameConsumer.training_waiting_room[0]
			RemoteGameConsumer.training_waiting_room.pop(0)
			game_group = await GameHandler.create(player1, player)
			asyncio.ensure_future(game_group.start_game())
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
				asyncio.ensure_future(game_group.start_game())
			else:
				RemoteGameConsumer.ranked_waiting_room.append(player)
			await player.send_state()
	
	# This function is called when a new connection is established
	# Checks if user is authenticated or not
	# If authenticated, checks if user is already connected with another device
	async def connect(self):
		await self.accept()
		if self.scope["user"].is_authenticated:
			username = self.scope["user"].username
			if Player.get_channel_by_user(self.scope["user"]) != None:
				await self.send(text_data=json.dumps({
					'type': 'redirect',
					'page': "other_device",
				}))
				print(f"User {self.scope['user'].id} connected to game-websocket with another device.")
				return
			player = Player(self.scope["user"], self.channel_name)
			await player.send_state()
			print(f"{self.scope['user'].username} connected to game-websocket.")
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
				# message handling for players in a game
				if player.get_game_handler() != None:
					if (data.get('type') == 'give_up'):
						player.get_game_handler().give_up(player)
					elif (data.get('type') == 'key_pressed' or data.get('type') == 'key_released'):
						player.get_game_handler().update_paddle(player, data.get('key'), data.get('type'))
				# message handling for players in the menu
				else:
					if data.get('type') == 'start_training_game':
						await self.add_to_training_waiting_room(player)
					elif data.get('type') == 'start_ranked_game':
						await self.add_to_ranked_waiting_room(player)
					elif data.get('type') == 'start_local_game':
						game_group = await GameHandler.create(player, player)
						asyncio.ensure_future(game_group.start_game())
		except json.JSONDecodeError:
			print(f"Error handling received message from a game-websocket: {text_data}")
	
	# This function is called when the connection is closed
	# Removes the player from game and waiting room and deletes the player object
	async def disconnect(self, close_code):
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
			print(f"{self.scope['user'].username} disconnected from game-websocket.")


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
