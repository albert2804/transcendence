import random
import math
import asyncio

class GPongGame:
	def __init__(self):
		self.pointsP1 = 0
		self.pointsP2 = 0
		self.isGameExited = False
		self.countdownSec = 2
		self.factor = 3 # by raising the factor the game is faster paced
		self.initialSpeed = 2 / self.factor
		self.currentSpeed = self.initialSpeed
		self.canvasWidth = 800
		self.canvasHeight = 400
		self.winner = 0
		
		# Game state saved as json (ready to be sent to the client)
		self.latest_game_state = None
		self.game_state_lock = asyncio.Lock() # Lock to prevent race conditions

		# Paddle initialization
		# self.leftPaddle = {'x': 0, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
		self.leftPaddle = {'x': 0, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
		self.rightPaddle = {'x': self.canvasWidth - 10, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}

		# Ball initialization
		self.acceleration = 0.05
		self.tolerance = 3
		self.velocity = 3
		self.max_velocity = 10
		self.ball = {'x': self.canvasWidth/2, 'y': self.canvasHeight/2, 'dx': self.velocity, 'dy': self.initialSpeed, 'radius': 6}

		# if there is an intersection of the ball and the paddle, intersection = true(needed for sound)
		self.intersection = False
		self.repel = 2 # the bigger the value the stronger the ball will be accelerated to the top after hitting a paddle
		
		# Game state saved as json (ready to be sent to the client)
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
		# self.ball['x'] += (self.ball['dx'])
		self.ball['x'] += self.ball['dx']
		
		acceleration = self.acceleration
		self.ball['dy'] += acceleration
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
			self.intersection = True
			self.gravity(self.leftPaddle)

		if (
			self.rightPaddle['x'] - self.ball['x'] < tolerance
			and (self.ball['y'] > self.rightPaddle['y'] and self.ball['y'] < (self.rightPaddle['y'] + self.rightPaddle['height']))
		):
			self.intersection = True
			self.gravity(self.rightPaddle)

		# Check for scoring
		if (self.ball['x'] - self.ball['radius'] < 0 ) and not self.intersection or (self.ball['x'] + self.ball['radius'] > self.canvasWidth) and not self.intersection :
			# Reset speed
			self.ball['dy'] = self.initialSpeed

			# Reset speed and ball direction depending on the person scoring
			if self.ball['x'] + self.ball['radius'] > self.canvasWidth:
				self.pointsP1 += 1
				self.ball['dx'] = -self.velocity
			elif self.ball['x'] - self.ball['radius'] < 0:
				self.pointsP2 += 1
				self.ball['dx'] = self.velocity

			# Reset ball position to center
			self.ball['x'] = self.canvasWidth/2
			self.ball['y'] = self.canvasHeight/2

		# Ensure the ball stays within the canvas after scoring
		self.ball['x'] = max(self.ball['radius'], min(self.canvasWidth - self.ball['radius'], self.ball['x']))


	def gravity(self, paddle):
		
		angle = (self.ball['dy']) / abs(self.ball['dx'])
		if (math.degrees(angle)) > 60:
			angle = math.pi / 3 
		elif (math.degrees(angle)) < -60:
			angle = -math.pi / 3 
		print(f"{math.degrees(angle)=}")

		# calculates the relative position of the ball to paddles on intersection -> value between 0 and 1
		pos = abs(self.ball['y'] - (paddle['y'] + paddle['height']/2)) / (paddle['height'] / 2)
		
		# calculates the repel, depending on the intersection point
		repel = (self.repel - pos)
	# very small angle ,less then 6 degrees = 0.1
		if angle <= 0.1 and angle >= -0.1:
			repel *= 1.5
		self.ball['dy'] = angle * repel * abs(self.ball['dx'])
		self.ball['dx'] = -self.ball['dx']  # Reverse the horizontal direction
		print(f"\n({self.ball['y']} - ({paddle['y']} + {paddle['height']/2})) / {paddle['height'] / 2}  = {pos}")
		print(f"Angle: {angle}")
		print(f"Repel: {repel}")
		print(f"\n OLD [DY]{self.ball['dy']}")
		print(f"\n NEW [DY]{self.ball['dy']}")
		print(f"\n{self.intersection=}")
		self.intersection = False
		
	
	def paddle_up(self, player):
		if player == 1:
			self.leftPaddle['dy'] = -6 / self.factor
		elif player == 2:
			self.rightPaddle['dy'] = -6 / self.factor
	
	def paddle_down(self, player):
		if player == 1:
			self.leftPaddle['dy'] = 6 / self.factor
		elif player == 2:
			self.rightPaddle['dy'] = 6 / self.factor
	
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

		# start countdown
		asyncio.create_task(self.countdown())
		# game loop
		import time
		while not self.isGameExited:
			self.game_loop()
			await self.save_game_state()
			await asyncio.sleep(0.02 / self.factor)
	
	async def countdown(self):
		while self.countdownSec > 0:
			await asyncio.sleep(1)
			self.countdownSec -= 1
