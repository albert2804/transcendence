from .gameHandler import GameHandler
from channels.layers import get_channel_layer

# This class represents a player in the RemoteGameConsumer
# Each registered user has one Player object that gets created when the user connects to the game websocket
#
# The Player object has only one channel (device) but you can change it with change_channel()
# The Player can be in only one game group at a time!

class Player:
	all_players = []

	# Returns the player object of the given channel
	@classmethod
	def get_player_by_channel(cls, channel):
		for player in Player.all_players:
			if player.get_channel() == channel:
				return player
		return None

	# Returns the channel of the given user
	@classmethod
	def get_channel_by_user(cls, user):
		for player in Player.all_players:
			if player.get_user() == user:
				return player.get_channel()
		return None

	# Returns the player object of the given user
	@classmethod
	def get_player_by_user(cls, user):
		for player in Player.all_players:
			if player.get_user() == user:
				return player
		return None

	# Constructor for the Player object
	def __init__(self, user, channel):
		self.user = user
		self.alias = user.alias
		self.alias_2 = None # for guest player in local game
		self.channel = channel
		self.channel_layer = get_channel_layer()
		self.game_handler = None
		self.fps = 40 # default fps is (60), the higher the more often data is transmitted to the frontend
		Player.all_players.append(self)
	
	# Getter for the user object (CustomUser) of the player
	def get_user(self):
		return self.user

	# Getter for the channel of the player
	def get_channel(self):
		return self.channel
	
	# This function sends the actual state of the player to his channel)
	async def send_state(self):
		from .consumers import RemoteGameConsumer
		# check if playing
		if self.game_handler != None:
			group = GameHandler.get_game_handler_by_name(self.game_handler)
			await self.send({
				'type': 'player_names',
				'p1_name': group.player1.alias,
				'p2_name': group.player2.alias,
			})
			await self.send({
				'type': 'redirect',
				'page': "playing",
			})
		# check if in waiting room or ranked waiting room
		elif (self in RemoteGameConsumer.training_waiting_room or self in RemoteGameConsumer.ranked_waiting_room
			or self in RemoteGameConsumer.training_waiting_room_g or self in RemoteGameConsumer.ranked_waiting_room_g):
			await self.send({
				'type': 'redirect',
				'page': "waiting",
			})
		# else send menu state
		else:
			await self.send({
				'type': 'redirect',
				'page': "menu",
			})

	# This function changes the channel of the player to the new_channel (device)
	async def change_channel(self, new_channel):
		await self.send({
			'type': 'redirect',
			'page': "other_device",
		})
		print(f"Player {self.user.alias} changed his device/channel")
		if self.game_handler != None:
			await self.channel_layer.group_discard(self.game_handler, self.channel)
			await self.channel_layer.group_add(self.game_handler, new_channel)
		self.channel = new_channel
		# send actual state to the new channel
		await self.send_state()
	
	# This function returns the game_handler of the player
	# If the player is not in a game group, it returns None !
	def get_game_handler(self):
		return GameHandler.get_game_handler_by_name(self.game_handler)
	
	# Function to send a message to the player
	async def send(self, message):
		await self.channel_layer.send(self.channel, message)
