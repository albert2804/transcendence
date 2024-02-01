import random
import asyncio
from .pong import PongGame
from channels.layers import get_channel_layer

# This class is used to handle the PongGame between the two Player objects (player1 and player2)
# Create a new instance of this class with GAME_XXX = GameHandler.create(player1, player2)
# Start this created instance with asyncio.ensure_future(GAME_XXX.start_game())
# After the game is finished, the instance gets deleted automatically
# To stop the game manually, use GAME_XXX.stop_game() (this will also delete the instance)

# TODO: implement a bool to decide if the game is a training game or a ranked game

class GameHandler:
	all_game_groups = {}

	# Use create() instead of __init__() to create a new instance of this class 
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.game_group = f"game_{random.randint(0, 1000000)}"
		self.game = PongGame()
		self.channel_layer = get_channel_layer()
		GameHandler.all_game_groups[self.game_group] = self

	@classmethod
	async def create(cls, player1, player2):
		instance = cls(player1, player2)
		# add players to game group (channel layer for sending messages to both players)
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
		return instance
	
	@classmethod
	def get_game_handler_by_name(cls, game_group_name):
		return cls.all_game_groups.get(game_group_name, None)

	async def start_game(self):
		print(f"Started {self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username}.")
		# send info, that game is starting
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'state',
				'state': "playing",
				'p1_name': self.player1.get_username(),
				'p2_name': self.player2.get_username(),
			}
		)
		# run game loop
		while not self.game.isGameExited:
			self.game.game_loop()
			await self.send_game_state()
			await asyncio.sleep(0.004)
		# send info, that game is finished
		if (self.game.winner == 0):
			await self.player1.send({
				'type': 'tied',
			})
			await self.player2.send({
				'type': 'tied',
			})
		elif (self.game.winner == 1):
			# player 1 won
			await self.player1.send({
				'type': 'winner',
			})
			await self.player2.send({
				'type': 'loser',
			})
		elif (self.game.winner == 2):
			await self.player1.send({
				'type': 'loser',
			})
			await self.player2.send({
				'type': 'winner',
			})
		print(f"{self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username} finished.")
		# wait 5 seconds
		await asyncio.sleep(5)
		# send info, that game is finished and players are back in the menu
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'state',
				'state': "menu",
				'p1_name': "",
				'p2_name': "",
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
		# print(f"Stopped game ({self.game_group}) between {self.player1.get_user().username} and {self.player2.get_user().username}.")
		self.game.isGameExited = True
	
	def update_paddle(self, player, key, type):
		if player == self.player1:
			if type == 'key_pressed':
				if key == 'ArrowUp':
					self.game.leftPaddle['dy'] = -2
				elif key == 'ArrowDown':
					self.game.leftPaddle['dy'] = 2
			elif type == 'key_released':
				if key in ['ArrowDown', 'ArrowUp']:
					self.game.leftPaddle['dy'] = 0
		elif player == self.player2:
			if type == 'key_pressed':
				if key == 'ArrowUp':
					self.game.rightPaddle['dy'] = -2
				elif key == 'ArrowDown':
					self.game.rightPaddle['dy'] = 2
			elif type == 'key_released':
				if key in ['ArrowDown', 'ArrowUp']:
					self.game.rightPaddle['dy'] = 0
		else:
			print(f"Unknown player: {player}")

	# send game state to game group (converted to percent)
	async def send_game_state(self):
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
			'numberOfHitsP1': self.game.numberOfHitsP1,
			'numberOfHitsP2': self.game.numberOfHitsP2,
		}
		# send game state to game group
		await self.channel_layer.group_send(
			self.game_group,
			{
				'type': 'game_update',
				'state': state,
				'high_score': high_score,
			}
		)