import random
import math
import asyncio

class PongGame:
	def __init__(self):
		self.pointsP1 = 0
		self.pointsP2 = 0
		self.isGameExited = False
		self.countdownSec = 5
		self.initialSpeed = 4
		self.currentSpeed = self.initialSpeed
		self.canvasWidth = 800
		self.canvasHeight = 400
		self.winner = 0

		# Game state saved as json (ready to be sent to the client)
		self.latest_game_state = None
		self.game_state_lock = asyncio.Lock() # Lock to prevent race conditions

		# Paddle initialization
		self.leftPaddle = {'x': 0, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
		self.rightPaddle = {'x': self.canvasWidth - 10, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}

		# Ball initialization
		self.ball = {'x': self.canvasWidth/2, 'y': self.canvasHeight/2, 'dx': self.initialSpeed, 'dy': self.initialSpeed, 'radius': 6}


	def update_game(self):
		# Update paddle positions
		self.leftPaddle['y'] += self.leftPaddle['dy']
		self.rightPaddle['y'] += self.rightPaddle['dy']

		# Ensure paddles stay within the canvas
		self.leftPaddle['y'] = max(0, min(self.canvasHeight - self.leftPaddle['height'], self.leftPaddle['y']))
		self.rightPaddle['y'] = max(0, min(self.canvasHeight - self.rightPaddle['height'], self.rightPaddle['y']))

		if self.countdownSec > 0:
			return
	
		# Move the ball
		self.ball['x'] += self.ball['dx']
		self.ball['y'] += self.ball['dy']

		# Bounce off the top or bottom of the canvas
		if self.ball['y'] - self.ball['radius'] < 0 or self.ball['y'] + self.ball['radius'] > self.canvasHeight:
			self.ball['dy'] = -self.ball['dy']
		
			# Ensure the ball stays within the canvas after bouncing off the bottom
			self.ball['y'] = max(self.ball['radius'], min(self.canvasHeight - self.ball['radius'], self.ball['y']))


		# Bounce off paddles and increase ball speed
		if (
			self.ball['x'] - self.ball['radius'] < self.leftPaddle['x'] + self.leftPaddle['width'] and
			self.leftPaddle['y'] < self.ball['y'] < self.leftPaddle['y'] + self.leftPaddle['height']
		):
			self.adjust_ball_angle(self.leftPaddle)

		if (
			self.ball['x'] + self.ball['radius'] > self.rightPaddle['x'] and
			self.rightPaddle['y'] < self.ball['y'] < self.rightPaddle['y'] + self.rightPaddle['height']
		):
			self.adjust_ball_angle(self.rightPaddle)

		# Check for scoring
		if self.ball['x'] - self.ball['radius'] < 0 or self.ball['x'] + self.ball['radius'] > self.canvasWidth:
			# Reset speed
			self.currentSpeed = self.initialSpeed
			self.ball['dy'] = self.currentSpeed

			# Reset speed and ball direction depending on the person scoring
			if self.ball['x'] + self.ball['radius'] > self.canvasWidth:
				self.pointsP1 += 1
				self.ball['dx'] = -self.currentSpeed
			elif self.ball['x'] - self.ball['radius'] < 0:
				self.pointsP2 += 1
				self.ball['dx'] = self.currentSpeed

			# Reset ball position to center
			self.ball['x'] = self.canvasWidth/2
		# Ensure the ball stays within the canvas after scoring
		self.ball['x'] = max(self.ball['radius'], min(self.canvasWidth - self.ball['radius'], self.ball['x']))
	
	def paddle_up(self, player):
		if player == 1:
			self.leftPaddle['dy'] = -6
		elif player == 2:
			self.rightPaddle['dy'] = -6
	
	def paddle_down(self, player):
		if player == 1:
			self.leftPaddle['dy'] = 6
		elif player == 2:
			self.rightPaddle['dy'] = 6
	
	def paddle_stop(self, player):
		if player == 1:
			self.leftPaddle['dy'] = 0
		elif player == 2:
			self.rightPaddle['dy'] = 0

	def game_loop(self):
		if self.pointsP1 < 3 and self.pointsP2 < 3:
			self.update_game()
		else:
			if self.pointsP1 == 3:
				self.winner = 1
			elif self.pointsP2 == 3:
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
		# start countdown
		asyncio.create_task(self.countdown())
		# game loop
		while not self.isGameExited:
			self.game_loop()
			await self.save_game_state()
			await asyncio.sleep(0.01)
	
	async def countdown(self):
		while self.countdownSec > 0:
			await asyncio.sleep(1)
			self.countdownSec -= 1

	# make game more interesting by adding different angles
	def adjust_ball_angle(self, paddle):
		angle_factor = (self.ball['y'] - paddle['y'] - paddle['height'] / 2) / (paddle['height'] / 2)
		max_angle = math.pi / 3  # Maximum angle change (adjust as needed)

		# Increase ball speed
		self.currentSpeed = min(self.currentSpeed + 1, 9)
		
		# Change the ball's angle based on the position on the paddle
		self.ball['dy'] = self.currentSpeed * angle_factor
		self.ball['dy'] = min(max(self.ball['dy'], -max_angle), max_angle)
		self.ball['dx'] = -self.ball['dx']  # Reverse the horizontal direction

		if self.ball['dx'] > 0:
			self.ball['dx'] = self.currentSpeed
		else:
			self.ball['dx'] = -self.currentSpeed
		
		

