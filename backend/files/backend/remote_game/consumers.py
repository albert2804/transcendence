from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .player import Player
from .gameHandler import GameHandler

from asgiref.sync import sync_to_async

# TODO: send user object or id instead of p1_channel and p2_channel to GameGroup.
#       this way the game can be continued if the user disconnects and reconnects
#       (the user object is still the same, but the channel name changes)
#       -> we can still send messages to the user with his private channel name (f"game_user_{user.id}")
#       -> also we don't need to use the "channel_to_user" from RemoteGameConsumer here in GameGroup !

# TODO: In Frontend: if websocket connection is closed -> show message "Connection lost. Please reload the page."
#       hmm maybe send a disconnection code to the frontend and show a message there (for example if the user is already connected with another device)
#       google about close_code for the disconnect function ;)

# TODO: maybe implement a static function in the Player class to remove a player from the list of all players
#       so we can stop the game automatically if the user disconnects
#       Other idea: do not delete the player from the list of all players directly, but "pause" the game and wait for the user to reconnect

# TODO: implement send() function in GameGroup to send to both players. maybe other name for this function?




class RemoteGameConsumer(AsyncWebsocketConsumer):

	# list of players in the waiting group
	waiting_room = []

	async def create_guest_player(self, alias):
		for p in Player.all_players:
			if p.get_user().username == alias:
				# player with this alias already exists
				await self.send(text_data=json.dumps({
					'type': 'alias_exists',
				}))
				return
		from api.models import CustomUser
		exists = await sync_to_async(CustomUser.objects.filter(username=alias).exists)()
		if exists:
			# CustomUser with this username already exists
			await self.send(text_data=json.dumps({
				'type': 'alias_exists',
			}))
			return
		# create new player object
		player = Player(self.scope["user"], self.channel_name)
		player.get_user().username = alias
		await player.send_state()
		print(f"Anonymous user upgraded to guest player with alias {alias}.")

	async def add_to_waiting_room(self, player):
		if len(RemoteGameConsumer.waiting_room) >= 1:
			player1 = RemoteGameConsumer.waiting_room[0]
			RemoteGameConsumer.waiting_room.pop(0)
			game_group = await GameHandler.create(player1, player)
			asyncio.ensure_future(game_group.start_game())
		else:
			RemoteGameConsumer.waiting_room.append(player)
		await player.send_state()
	
	async def connect(self):
		await self.accept()
		if self.scope["user"].is_authenticated:
			username = self.scope["user"].username
			if Player.get_channel_by_user(self.scope["user"]) != None:
				# user is already connected with another device (same user, different channel)
				await self.send(text_data=json.dumps({
					'type': 'state',
					'state': "other_device",
					'p1_name': "",
					'p2_name': "",
				}))
				print(f"User {self.scope['user'].id} connected to game-websocket with another device.")
				return
			# create new player object
			player = Player(self.scope["user"], self.channel_name)
			await player.send_state()
			print(f"{self.scope['user'].username} connected to game-websocket.")
		else:
			print(f"Anonymous user connected to game-websocket.")
			# send state to bring guest to an alias screen !
			await self.send(text_data=json.dumps({
				'type': 'alias_screen',
			}))
	
	async def receive(self, text_data):
		try:
			player = Player.get_player_by_channel(self.channel_name)
			if player == None:
				# print(f"Received message from unknown player: {text_data}")
				if self.scope["user"].is_authenticated:
					# authenticated but no player object -> already connected with another device
					data = json.loads(text_data)
					if data.get('type') == 'change_device':
						# change channel (device) to this one
						if Player.get_channel_by_user(self.scope["user"]) != None:
							oldchannel = Player.get_channel_by_user(self.scope["user"])
							player = Player.get_player_by_channel(oldchannel)
							await player.change_channel(self.channel_name)
				# return
				else:
					# print(f"Received message from unauthorized user: {text_data}")
					# not authenticated -> create guest player
					data = json.loads(text_data)
					if data.get('type') == 'create_guest_player':
						await self.create_guest_player(data.get('alias'))
			# check if player is in a game group
			elif player.get_game_handler() != None:
				# get the game data
				game_data = json.loads(text_data)
				# update the paddle
				player.get_game_handler().update_paddle(player, game_data.get('key'), game_data.get('type'))
			else:
				# get the menu data
				menu_data = json.loads(text_data)
				# check if the user wants to start a game
				if menu_data.get('type') == 'start_game':
					await self.add_to_waiting_room(player)
				else:
					print(f"Received invalid JSON file: {menu_data}")
		except json.JSONDecodeError:
			print(f"Error handling received message from a game-websocket: {text_data}")
		
	async def disconnect(self, close_code):
		# if self.scope["user"].is_authenticated:
		player = Player.get_player_by_channel(self.channel_name)
		if player != None:
			# Stop the game if the user is in a game group (LATER CHANGE THIS TO WAIT A FEW SECONDS AND CHECK IF THE USER RECONNECTS)
			if player.get_game_handler() != None:
				print(f"Stopping game group: {player.get_game_handler()}")
				player.get_game_handler().stop_game()
			# remove player from waiting room list if in there
			if player in RemoteGameConsumer.waiting_room:
				RemoteGameConsumer.waiting_room.remove(player)
			# remove player from list of all players
			Player.all_players.remove(Player.get_player_by_channel(self.channel_name))
			print(f"{self.scope['user'].username} disconnected from game-websocket.")


	#########################
	# group message handler #
	#########################
	
	# This "state" message is used to redirect the user to the specific page (menu, waiting, game, other_device)
	async def state(self, event):
		await self.send(text_data=json.dumps({
			'type': 'state',
			'state': event['state'], # "playing", "waiting", "menu", "other_device"
			'p1_name': event['p1_name'],
			'p2_name': event['p2_name'],
		}))
	
	# This "game_update" message is used to update the game state
	# The players needs to be in the "playing" state to receive this message
	async def game_update(self, event):
		await self.send(text_data=json.dumps({
			'type': 'game_update',
			'state': event['state'],
			'high_score': event['high_score'],
		}))
	
	# "winner", "loser" and "tied" are used to show the winner/loser/tied screen
	# 5 seconds after the game is finished the players also get redirected to the menu (gets the "menu" state message)
	async def winner(self, event):
		await self.send(text_data=json.dumps({
			'type': 'winner',
		}))
	
	async def loser(self, event):
		await self.send(text_data=json.dumps({
			'type': 'loser',
		}))
	
	async def tied(self, event):
		await self.send(text_data=json.dumps({
			'type': 'tied',
		}))

	# Only for guest players
	async def alias_screen(self, event):
		await self.send(text_data=json.dumps({
			'type': 'alias_screen',
		}))

	async def alias_exists(self, event):
		await self.send(text_data=json.dumps({
			'type': 'alias_exists',
		}))
