import random
import asyncio
from .pong import PongGame
from chat.consumers import ChatConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model

# This class is used to handle the PongGame between the two Player objects (player1 and player2)
# Create a new instance of this class with GAME_XXX = GameHandler.create(player1, player2)
# Start this created instance with asyncio.ensure_future(GAME_XXX.start_game())
# After the game is finished, the instance gets deleted automatically

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
		# ? Why random.randint?
		self.game_group = f"game_{random.randint(0, 1000000)}"
		self.game = PongGame()
		self.channel_layer = get_channel_layer()
		GameHandler.all_game_groups[self.game_group] = self
		self.pressed_keys_p1 = []
		self.pressed_keys_p2 = []
		# only used for ranked games:
		self.ranked = ranked
		self.db_entry = None
		self.game_start_time = None

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
		# create db entry if ranked (the rest will be filled after the game is finished)
		if ranked:
			from .models import RemoteGame
			instance.db_entry = await sync_to_async(RemoteGame.objects.create)(
				player1=player1.get_user(),
				player2=player2.get_user(),
			)
		return instance
	
	@classmethod
	def create_tournament_game(cls, player1, player2, ranked=False):
		return 

	# Returns the game handler instance from the given game group name
	@classmethod
	def get_game_handler_by_name(cls, game_group_name):
		return cls.all_game_groups.get(game_group_name, None)
	
	# gets called at start of the game
	async def send_player_names(self):
		if self.local_game:
			player1_name = self.player1.alias
			player2_name = self.player1.alias_2
		else:
			if self.player1.get_user().is_authenticated:
				player1_name = self.player1.alias
			else:
				player1_name = self.player1.alias + " (guest)"
			if self.player2.get_user().is_authenticated:
				player2_name = self.player2.alias
			else:
				player2_name = self.player2.alias + " (guest)"
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

	# send the game rusult to the players chat
	async def send_game_result_to_chat(self):
		chat_consumer = ChatConsumer()
		if self.ranked:
			# get the points of the players
			p1_points = int(self.game.pointsP1)
			p2_points = int(self.game.pointsP2)
			# send the game result to the chat
			if self.game.winner == 0:
				await chat_consumer.save_and_send_message(self.player1.get_user(), self.player2.get_user(), "A ranked game ended in a tie.", timezone.now(), "info")
				await chat_consumer.save_and_send_message(self.player2.get_user(), self.player1.get_user(), "A ranked game ended in a tie.", timezone.now(), "info")
			elif self.game.winner == 1:
				await chat_consumer.save_and_send_message(self.player2.get_user(), self.player1.get_user(), "You won a ranked game with " + str(p1_points) + " to " + str(p2_points) + " points.", timezone.now(), "info")
				await chat_consumer.save_and_send_message(self.player1.get_user(), self.player2.get_user(), "You lost a ranked game with " + str(p2_points) + " to " + str(p1_points) + " points.", timezone.now(), "info")
			elif self.game.winner == 2:
				await chat_consumer.save_and_send_message(self.player1.get_user(), self.player2.get_user(), "You won a ranked game with " + str(p2_points) + " to " + str(p1_points) + " points.", timezone.now(), "info")
				await chat_consumer.save_and_send_message(self.player2.get_user(), self.player1.get_user(), "You lost the game with " + str(p1_points) + " to " + str(p2_points) + " points.", timezone.now(), "info")
				

	# Starts the game and runs the game loop until the game is finished or stopped
	async def start_game(self):
		self.game_start_time = timezone.now()
		if self.local_game:
			print(f"Started local game {self.game_group} --- {self.player1.get_user().alias}.")
		elif self.ranked:
			print(f"Started ranked {self.game_group} between {self.player1.get_user().alias} and {self.player2.get_user().alias}.")
		else:
			print(f"Started {self.game_group} between {self.player1.get_user().alias} and {self.player2.get_user().alias}.")
		# send player names to game group
		await self.send_player_names()
		# send redirect to playing page
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'redirect',
				'page': "playing",
			})
		# start two separate threads for sending the game state to player 1 and player 2
		# I used separate threads because so we can handle different fps for each player
		asyncio.ensure_future(self.send_game_state_to_player_1())
		asyncio.ensure_future(self.send_game_state_to_player_2())
		# run the game loop until the game is finished
		await self.game.run_game()
		# if ranked game, fill the db entry
		if self.ranked:
			await self.save_result_to_db()
		if self.local_game:
			self.player1.alias_2 = None
			print(f"Local game {self.game_group} finished.")
		elif self.ranked:
			print(f"Ranked {self.game_group} between {self.player1.get_user().alias} and {self.player2.get_user().alias} finished.")
		else:
			print(f"{self.game_group} between {self.player1.get_user().alias} and {self.player2.get_user().alias} finished.")
		# send game result to game group
		await self.send_game_result()
		# send game result to the chat (only for ranked games)
		await self.send_game_result_to_chat()
		# wait 2 seconds
		await asyncio.sleep(2)
		# redirect players to menu
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'redirect',
				'page': "menu",
			})
		# remove players from game group (channel layer for both players)
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
	
	# saves the game result to the db entry (only for ranked games)
	async def save_result_to_db(self):
		from .models import RemoteGame
		# fill the db entry with the game result
		self.db_entry.started_at = self.game_start_time
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
		await sync_to_async(self.db_entry.save)()
		# update the user stats in CustomUser
		db_p1_user = await database_sync_to_async(get_user_model().objects.get)(id=self.player1.get_user().id)
		db_p2_user = await database_sync_to_async(get_user_model().objects.get)(id=self.player2.get_user().id)
		db_p1_user.num_games_played += 1
		db_p2_user.num_games_played += 1
		if self.game.winner == 1:
			db_p1_user.num_games_won += 1
		elif self.game.winner == 2:
			db_p2_user.num_games_won += 1
		await database_sync_to_async(db_p1_user.save)()
		await database_sync_to_async(db_p2_user.save)()

	# This function is called when a player gives up or disconnects
	# The other player wins the game
	def give_up(self, player):
		if not self.local_game:
			if player == self.player1:
				self.game.winner = 2
			else:
				self.game.winner = 1
		self.game.isGameExited = True
	
	# This function is called when a player wants to update the paddle position
	# (gets called from consumers.py receive(), when a player sends a message)
	def update_paddle(self, player, key, type):
		if not key in ['ArrowUp', 'ArrowDown', 'w', 's']:
			return
    	# if local game, check which paddle to update because of the key
		if self.local_game:
			if key in ['w', 's']:
				pressed_keys = self.pressed_keys_p1
				paddle_num = 1
			elif key in ['ArrowUp', 'ArrowDown']:
				pressed_keys = self.pressed_keys_p2
				paddle_num = 2
		# if remote game, check which paddle to update because of the player object
		else:
			if player == self.player1:
				pressed_keys = self.pressed_keys_p1
				paddle_num = 1
			elif player == self.player2:
				pressed_keys = self.pressed_keys_p2
				paddle_num = 2
		# update the paddle position
		if type == 'key_pressed':
			if key in pressed_keys:
				pressed_keys.remove(key)
			pressed_keys.append(key)
		elif type == 'key_released':
			if key in pressed_keys:
				pressed_keys.remove(key)
		if pressed_keys:
			last_key = pressed_keys[-1]
			if last_key in ['ArrowUp', 'w']:
				self.game.paddle_up(paddle_num)
			elif last_key in ['ArrowDown', 's']:
				self.game.paddle_down(paddle_num)
		else:
			self.game.paddle_stop(paddle_num)
	
	# sends the latest game state to player 1
	# gets called in a separate thread
	async def send_game_state_to_player_1(self): 
		while not self.game.isGameExited:
			async with self.game.game_state_lock:
				game_state = self.game.latest_game_state
			if game_state is not None:
				await self.player1.send(game_state)
			await asyncio.sleep(1 / self.player1.fps)
	
	# sends the latest game state to player 2
	# gets called in a separate thread
	async def send_game_state_to_player_2(self):
		while not self.game.isGameExited:
			async with self.game.game_state_lock:
				game_state = self.game.latest_game_state
			if game_state is not None:
				await self.player2.send(game_state)
			await asyncio.sleep(1 / self.player2.fps)