import random
import math
import asyncio

class PongGame:
	def __init__(self):
		self.started = False
		self.paused = False
		self.pointsP1 = 0
		self.pointsP2 = 0
		self.isGameExited = False
		self.countdownSec = 3
		self.factor = 3.5 # by raising the factor the game is faster paced
		self.initialSpeed = 4 / self.factor
		self.canvasWidth = 800
		self.canvasHeight = 400
		self.winner = 0
		
		# Game state saved as json (ready to be sent to the client)
		self.latest_game_state = None
		self.game_state_lock = asyncio.Lock() # Lock to prevent race conditions

		# Paddle initialization
		self.leftPaddle = {'x': 0, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
		self.rightPaddle = {'x': self.canvasWidth - 10, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
		self.paddle_speed = 12
		# Ball initialization
		self.acceleration = 1.2
		self.tolerance = 5
		self.max_velocity = 15 / self.factor
		self.ball = {'x': self.canvasWidth/2, 'y': self.canvasHeight/2, 'dx': self.initialSpeed, 'dy': self.initialSpeed, 'radius': 6}

		# if there is an intersection of the ball and the paddle, intersection = true(needed for sound)
		self.intersection = False

		# Game state saved as json (ready to be sent to the client)
	def update_game(self):

		if self.ball['x'] > self.canvasWidth / 2 - 50 and self.ball['x'] < self.canvasWidth / 2 + 50:
			self.intersection = False

		# Update paddle positions
		self.leftPaddle['y'] += self.leftPaddle['dy']
		self.rightPaddle['y'] += self.rightPaddle['dy']

		# Ensure paddles stay within the canvas
		self.leftPaddle['y'] = max(0, min(self.canvasHeight - self.leftPaddle['height'], self.leftPaddle['y']))
		self.rightPaddle['y'] = max(0, min(self.canvasHeight - self.rightPaddle['height'], self.rightPaddle['y']))

		if self.countdownSec > 0:
			return
	
		# Move the ball
		# self.ball['x'] += (self.ball['dx'])
		self.ball['x'] += self.ball['dx']
		self.ball['y'] += self.ball['dy']

		# Bounce off the top or bottom of the canvas
		if self.ball['y'] - self.ball['radius'] < 0 or self.ball['y'] + self.ball['radius'] > self.canvasHeight:
			self.ball['dy'] = (-self.ball['dy'])
		
			# Ensure the ball stays within the canvas after bouncing off the bottom
			self.ball['y'] = max(self.ball['radius'], min(self.canvasHeight - self.ball['radius'], self.ball['y']))

		# Bounce off paddles with some tolerance and increased ball speed
		tolerance = self.tolerance
		if ((self.ball['x']) - (self.leftPaddle['x'] + self.leftPaddle['width']) <  tolerance
				and (self.ball['y'] > self.leftPaddle['y'] and self.ball['y'] < (self.leftPaddle['y'] + self.leftPaddle['height']))
		):
			if not self.intersection:
				self.repel()
				self.intersection = True
				
		if (
			self.rightPaddle['x'] - self.ball['x'] < tolerance
			and (self.ball['y'] > self.rightPaddle['y'] and self.ball['y'] < (self.rightPaddle['y'] + self.rightPaddle['height']))
		):
			if not self.intersection:
				self.repel()
				self.intersection = True

		# Check for scoring
		if (self.ball['x'] - self.ball['radius'] < 0 ) and not self.intersection or (self.ball['x'] + self.ball['radius'] > self.canvasWidth) and not self.intersection :
			# Reset speed
			self.ball['dy'] = self.initialSpeed

			# Reset speed and ball direction depending on the person scoring
			if self.ball['x'] + self.ball['radius'] > self.canvasWidth:
				self.pointsP1 += 1
				self.ball['dx'] = self.ball['dy'] = -self.initialSpeed
			elif self.ball['x'] - self.ball['radius'] < 0:
				self.pointsP2 += 1
				self.ball['dx'] = self.ball['dy'] = -self.initialSpeed

			# Reset ball position to center
			self.ball['x'] = self.canvasWidth/2
			self.ball['y'] = self.canvasHeight/2

		# Ensure the ball stays within the canvas after scoring
		self.ball['x'] = max(self.ball['radius'], min(self.canvasWidth - self.ball['radius'], self.ball['x']))


	def repel(self):
		
		angle = (self.ball['dy']) / abs(self.ball['dx'])

		self.ball['dy'] = angle * abs(self.ball['dx'])
		self.ball['dx'] =-self.ball['dx']  # Reverse the horizontal direction
		if not abs(self.ball['dx']) > self.max_velocity:
			self.ball['dx'] *= self.acceleration # raise the velocity by a factor
		
	
	def paddle_up(self, player):
		if player == 1:
			self.leftPaddle['dy'] = -self.paddle_speed / self.factor
		elif player == 2:
			self.rightPaddle['dy'] = -self.paddle_speed / self.factor
	
	def paddle_down(self, player):
		if player == 1:
			self.leftPaddle['dy'] = self.paddle_speed / self.factor
		elif player == 2:
			self.rightPaddle['dy'] = self.paddle_speed / self.factor
	
	def paddle_stop(self, player):
		if player == 1:
			self.leftPaddle['dy'] = 0
		elif player == 2:
			self.rightPaddle['dy'] = 0

	def game_loop(self):
		if self.pointsP1 < 7 and self.pointsP2 < 7:
			self.update_game()
		else:
			if self.pointsP1 == 7:
				self.winner = 1
			elif self.pointsP2 == 7:
				self.winner = 2
			self.isGameExited = True

	async def save_game_state(self):
		state = {
			'ball': {
				'x': (self.ball['x'] / self.canvasWidth) * 100,
				'y': (self.ball['y'] / self.canvasHeight) * 100,
			},
			'leftPaddle': {
				'y': (self.leftPaddle['y'] / self.canvasHeight) * 100,
			},
			'rightPaddle': {
				'y': (self.rightPaddle['y'] / self.canvasHeight) * 100,
			},
			'countdown': self.countdownSec,
			'intersection': self.intersection,
		}
		high_score = {
			'pointsP1': self.pointsP1,
			'pointsP2': self.pointsP2,
		}
		async with self.game_state_lock:
			self.latest_game_state = {
				'type': 'game_update',
				'state': state,
				'high_score': high_score,
			}
	
	async def run_game(self):
		self.started = True
		# start countdown
		asyncio.create_task(self.countdown())
		# game loop
		import time
		while not self.isGameExited:
			if self.paused == False:
				self.game_loop()
			await self.save_game_state()
			await asyncio.sleep(0.02 / self.factor)
	
	async def countdown(self):
		while self.countdownSec > 0:
			await asyncio.sleep(1)
			self.countdownSec -= 1

