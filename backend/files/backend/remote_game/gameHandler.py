import random
import asyncio
from .pong import PongGame
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from django.utils import timezone

# This class is used to handle the PongGame between the two Player objects (player1 and player2)
# Create a new instance of this class with GAME_XXX = GameHandler.create(player1, player2)
# Start this created instance with asyncio.ensure_future(GAME_XXX.start_game())
# After the game is finished, the instance gets deleted automatically
# To stop the game manually, use GAME_XXX.stop_game() (this will also delete the instance)

# TODO: implement a bool to decide if the game is a training game or a ranked game

class GameHandler:
	all_game_groups = {}

	# Use create() instead of __init__() to create a new instance of this class 
	# @database_sync_to_async
	def __init__(self, player1, player2, ranked=False):
		self.player1 = player1
		self.player2 = player2
		if (player1 == player2):
			self.local_game = True
		else:
			self.local_game = False
		self.ranked = ranked
		self.db_entry = None
		self.game_group = f"game_{random.randint(0, 1000000)}"
		self.game = PongGame()
		self.channel_layer = get_channel_layer()
		GameHandler.all_game_groups[self.game_group] = self
		# This variable is used to store the latest game state
		# So we can store and send the latest game state to players instead of sending the whole game state
		# This is useful during network lag
		self.latest_game_state = None

	# Use this function to create a new instance of this class
	@classmethod
	async def create(cls, player1, player2, ranked=False):
		instance = cls(player1, player2, ranked)
		player1.game_handler = instance.game_group
		await instance.channel_layer.group_add(
			instance.game_group,
			player1.channel
		)
		player2.game_handler = instance.game_group
		await instance.channel_layer.group_add(
			instance.game_group,
			player2.channel
		)
		if ranked:
			from .models import RemoteGame
			instance.db_entry = await sync_to_async(RemoteGame.objects.create)(
				player1=player1.get_user(),
				player2=player2.get_user(),
			)
		return instance
	
	# Returns the game handler instance from the given game group name
	@classmethod
	def get_game_handler_by_name(cls, game_group_name):
		return cls.all_game_groups.get(game_group_name, None)
	
	# gets called at start of the game
	async def send_player_names(self):
		if self.local_game:
			player1_name = ""
			player2_name = ""
		else:
			player1_name = self.player1.get_username()
			player2_name = self.player2.get_username()
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'player_names',
				'p1_name': player1_name,
				'p2_name': player2_name
			})
	
	# sends the game result to the players
	# gets called after the game is finished
	async def send_game_result(self):
		if self.local_game:
			if (self.game.winner == 0):
				await self.player1.send({
					'type': 'game_result',
					'result': 'tied',
				})
			elif (self.game.winner == 1):
				await self.player1.send({
					'type': 'game_result',
					'result': 'left',
				})
			else:
				await self.player1.send({
					'type': 'game_result',
					'result': 'right',
				})
		elif (self.game.winner == 0):
			await self.player1.send({
				'type': 'game_result',
				'result': 'tied',
			})
			await self.player2.send({
				'type': 'game_result',
				'result': 'tied',
			})
		elif (self.game.winner == 1):
			await self.player1.send({
				'type': 'game_result',
				'result': 'winner',
			})
			await self.player2.send({
				'type': 'game_result',
				'result': 'loser',
			})
		elif (self.game.winner == 2):
			await self.player1.send({
				'type': 'game_result',
				'result': 'loser',
			})
			await self.player2.send({
				'type': 'game_result',
				'result': 'winner',
			})

	# Starts the game and runs the game loop until the game is finished or stopped
	async def start_game(self):
		if self.local_game:
			print(f"Started local game {self.game_group} --- {self.player1.get_user().username}.")
		elif self.ranked:
			print(f"Started ranked {self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username}.")
			# fill in the started_at field of the db entry
			from .models import RemoteGame
			self.db_entry.started_at = timezone.now()
			await sync_to_async(self.db_entry.save)()
			
		else:
			print(f"Started {self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username}.")
		# send player names to game group
		await self.send_player_names()
		# send redirect to playing page
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'redirect',
				'page': "playing",
			})
		# start send_from_queue in background
		# asyncio.ensure_future(self.send_from_queue())
		asyncio.ensure_future(self.send_game_state_to_player_1())
		asyncio.ensure_future(self.send_game_state_to_player_2())
		# run game loop
		while not self.game.isGameExited:
			self.game.game_loop()
			await self.save_game_state()
			await asyncio.sleep(0.01) # 100 times per second still too much?
		# send game result to game group
		await self.send_game_result()
		# if ranked game, fill the db entry
		if self.ranked:
			from .models import RemoteGame
			self.db_entry.finished_at = timezone.now()
			self.db_entry.pointsP1 = int(self.game.pointsP1)
			self.db_entry.pointsP2 = int(self.game.pointsP2)
			if self.game.winner == 1:
				self.db_entry.winner = self.player1.get_user()
				self.db_entry.loser = self.player2.get_user()
			elif self.game.winner == 2:
				self.db_entry.winner = self.player2.get_user()
				self.db_entry.loser = self.player1.get_user()
			self.db_entry.finished = True
			print("Hits Player 1:", self.game.pointsP1)
			print("Hits Player 2:", self.game.pointsP2)
			await sync_to_async(self.db_entry.save)()
		if self.local_game:
			print(f"Local game {self.game_group} finished.")
		elif self.ranked:
			print(f"Ranked {self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username} finished.")
		else:
			print(f"{self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username} finished.")
		# wait 5 seconds
		await asyncio.sleep(5)
		# send redirect to menu
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'redirect',
				'page': "menu",
			}
		)
		# remove players from game group (channel layer for sending messages to both players)
		await self.channel_layer.group_discard(
			self.game_group,
			self.player1.channel
		)
		self.player1.game_handler = None
		await self.channel_layer.group_discard(
			self.game_group,
			self.player2.channel
		)
		self.player2.game_handler = None
		# delete instance
		del GameHandler.all_game_groups[self.game_group]
		del self
	
	def stop_game(self):
		self.game.isGameExited = True
	
	# This function is called when a player wants to update the paddle position
	# (gets called from consumers.py receive(), when a player sends a message)
	def update_paddle(self, player, key, type):
		if self.local_game:
			if type == 'key_pressed':
				if key == 'ArrowUp':
					self.game.rightPaddle['dy'] = -4
				elif key == 'ArrowDown':
					self.game.rightPaddle['dy'] = 4
				elif key == 'w':
					self.game.leftPaddle['dy'] = -4
				elif key == 's':
					self.game.leftPaddle['dy'] = 4
			elif type == 'key_released':
				if key in ['ArrowDown', 'ArrowUp']:
					self.game.rightPaddle['dy'] = 0
				elif key in ['w', 's']:
					self.game.leftPaddle['dy'] = 0
		elif player == self.player1:
			if type == 'key_pressed':
				if key == 'ArrowUp':
					self.game.leftPaddle['dy'] = -4
				elif key == 'ArrowDown':
					self.game.leftPaddle['dy'] = 4
			elif type == 'key_released':
				if key in ['ArrowDown', 'ArrowUp']:
					self.game.leftPaddle['dy'] = 0
		elif player == self.player2:
			if type == 'key_pressed':
				if key == 'ArrowUp':
					self.game.rightPaddle['dy'] = -4
				elif key == 'ArrowDown':
					self.game.rightPaddle['dy'] = 4
			elif type == 'key_released':
				if key in ['ArrowDown', 'ArrowUp']:
					self.game.rightPaddle['dy'] = 0
		else:
			print(f"Unknown player: {player}")

	# saves the actual game state to latest_game_state
	async def save_game_state(self):
		state = {
			'ball': {
				'x': (self.game.ball['x'] / self.game.canvasWidth) * 100,
				'y': (self.game.ball['y'] / self.game.canvasHeight) * 100,
			},
			'leftPaddle': {
				'y': (self.game.leftPaddle['y'] / self.game.canvasHeight) * 100,
			},
			'rightPaddle': {
				'y': (self.game.rightPaddle['y'] / self.game.canvasHeight) * 100,
			},
		}
		high_score = {
			'pointsP1': self.game.pointsP1,
			'pointsP2': self.game.pointsP2,
		}
		# store latest game state
		self.latest_game_state = {
			'type': 'game_update',
			'state': state,
			'high_score': high_score,
		}

	# sends the latest game state to the game group
	async def send_from_queue(self):
		while not self.game.isGameExited:
			if self.latest_game_state is not None:
				await self.channel_layer.group_send(
					self.game_group,
					self.latest_game_state
				)
				self.latest_game_state = None
			# await asyncio.sleep(0.1)
			# await asyncio.sleep(0.05)
			await asyncio.sleep(0.025)
			# await asyncio.sleep(0.01)
			# await asyncio.sleep(0)
	
	async def send_game_state_to_player_1(self): 
		while not self.game.isGameExited: # ALSO CHECK FOR PLAYER != NONE ??
			if self.latest_game_state is not None:
				await self.player1.send(self.latest_game_state)
				self.latest_game_state = None
			# await asyncio.sleep(0.1)
			# await asyncio.sleep(0.05)
			await asyncio.sleep(0.025)
			# await asyncio.sleep(0.01)
			# await asyncio.sleep(0)
	
	async def send_game_state_to_player_2(self):
		while not self.game.isGameExited:
			if self.latest_game_state is not None:
				await self.player2.send(self.latest_game_state)
				self.latest_game_state = None
			await asyncio.sleep(0.1)
			# await asyncio.sleep(0.05)
			# await asyncio.sleep(0.025)
			# await asyncio.sleep(0.01)
			# await asyncio.sleep(0)