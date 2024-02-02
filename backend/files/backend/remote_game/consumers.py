from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .player import Player
from .gameHandler import GameHandler
from asgiref.sync import sync_to_async

# TODO: Implement a logic to wait (30sec?) for the user to reconnect if he disconnects before stopping the game
#	   	This is only possible with registered users (not guests) because we need to know the user id (or we have to implement a session management for guests... but this is way too much for now)

# TODO: In Frontend: if websocket connection is closed -> show message "Connection lost. Please reload the page."
#       hmm maybe send a disconnection code to the frontend and show a message there (for example if the user is already connected with another device)
#       google about close_code for the disconnect function ;)

# TODO: implement send() function in GameGroup to send to both players. maybe other name for this function?




class RemoteGameConsumer(AsyncWebsocketConsumer):

	# list of players in the waiting group (mixed room for guests and registered users -> unranked games)
	waiting_room = []

	# Tries to create a guest player with the given alias
	# If the alias is already taken, the player gets an "alias_exists" message
	async def create_guest_player(self, alias):
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

	# This function adds the player to the waiting room list
	async def add_to_waiting_room(self, player):
		if len(RemoteGameConsumer.waiting_room) >= 1:
			player1 = RemoteGameConsumer.waiting_room[0]
			RemoteGameConsumer.waiting_room.pop(0)
			game_group = await GameHandler.create(player1, player)
			asyncio.ensure_future(game_group.start_game())
		else:
			RemoteGameConsumer.waiting_room.append(player)
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
	
	# Message handler
	async def receive(self, text_data):
		try:
			player = Player.get_player_by_channel(self.channel_name)
			if player == None:
				if self.scope["user"].is_authenticated:
					data = json.loads(text_data)
					if data.get('type') == 'change_device':
						if Player.get_channel_by_user(self.scope["user"]) != None:
							oldchannel = Player.get_channel_by_user(self.scope["user"])
							player = Player.get_player_by_channel(oldchannel)
							await player.change_channel(self.channel_name)
				else:
					data = json.loads(text_data)
					if data.get('type') == 'create_guest_player':
						await self.create_guest_player(data.get('alias'))
			elif player.get_game_handler() != None:
				game_data = json.loads(text_data)
				player.get_game_handler().update_paddle(player, game_data.get('key'), game_data.get('type'))
			else:
				menu_data = json.loads(text_data)
				if menu_data.get('type') == 'start_game':
					await self.add_to_waiting_room(player)
				# else:
					# print(f"Received invalid JSON file: {menu_data}")      # uncommented because this also happens when the message is valid but not at the right time
		except json.JSONDecodeError:
			print(f"Error handling received message from a game-websocket: {text_data}")
	
	# This function is called when the connection is closed
	# Removes the player from game groups and waiting room and deletes the player object (LATER CHANGE THIS TO WAIT A FEW SECONDS AND CHECK IF THE USER RECONNECTS)
	async def disconnect(self, close_code):
		player = Player.get_player_by_channel(self.channel_name)
		if player != None:
			# Stop the game if the user is in a game group (LATER CHANGE THIS TO WAIT A FEW SECONDS AND CHECK IF THE USER RECONNECTS)
			if player.get_game_handler() != None:
				print(f"Stopping game group: {player.get_game_handler()}")
				player.get_game_handler().stop_game()
			if player in RemoteGameConsumer.waiting_room:
				RemoteGameConsumer.waiting_room.remove(player)
			Player.all_players.remove(Player.get_player_by_channel(self.channel_name))
			print(f"{self.scope['user'].username} disconnected from game-websocket.")


	#####################
	## MESSAGE HANDLER ##
	#####################
	
	# This message is used to redirect the players to the different pages of the pong game
	# "playing", "waiting", "menu", "other_device", "alias_screen",
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
