class PongGame:
    def __init__(self):
        self.numberOfHitsP1 = 0
        self.numberOfHitsP2 = 0
        self.isGameExited = False
        self.isGamePaused = False
        self.initialSpeed = 2
        self.currentSpeed = self.initialSpeed
        self.canvasWidth = 800
        self.canvasHeight = 400
        self.winner = 0

        # Paddle initialization
        self.leftPaddle = {'x': 0, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}
        self.rightPaddle = {'x': self.canvasWidth - 10, 'y': self.canvasHeight/2 - 40, 'dy': 0, 'width': 10, 'height': 80}

        # Ball initialization
        self.ball = {'x': self.canvasWidth/2, 'y': self.canvasHeight/2, 'dx': self.initialSpeed, 'dy': self.initialSpeed, 'radius': 6}



    def update_game(self):
        # If the game is paused, the game will not be updated
        if self.isGamePaused:
            return

        # Update paddle positions
        self.leftPaddle['y'] += self.leftPaddle['dy']
        self.rightPaddle['y'] += self.rightPaddle['dy']

        # Ensure paddles stay within the canvas
        self.leftPaddle['y'] = max(0, min(self.canvasHeight - self.leftPaddle['height'], self.leftPaddle['y']))
        self.rightPaddle['y'] = max(0, min(self.canvasHeight - self.rightPaddle['height'], self.rightPaddle['y']))

        # Move the ball
        self.ball['x'] += self.ball['dx']
        self.ball['y'] += self.ball['dy']

        # Bounce off the top or bottom of the canvas
        if self.ball['y'] - self.ball['radius'] < 0 or self.ball['y'] + self.ball['radius'] > self.canvasHeight:
            self.ball['dy'] = -self.ball['dy']

        # Bounce off paddles and increase ball speed
        if (
            self.ball['x'] - self.ball['radius'] < self.leftPaddle['x'] + self.leftPaddle['width'] and
            self.leftPaddle['y'] < self.ball['y'] < self.leftPaddle['y'] + self.leftPaddle['height']
        ):
            if self.currentSpeed < 6:
                self.currentSpeed += 0.5
            self.ball['dy'] = -self.currentSpeed
            self.ball['dx'] = self.currentSpeed
            # print('Current speed:', self.currentSpeed)

        if (
            self.ball['x'] + self.ball['radius'] > self.rightPaddle['x'] and
            self.rightPaddle['y'] < self.ball['y'] < self.rightPaddle['y'] + self.rightPaddle['height']
        ):
            if self.currentSpeed < 6:
                self.currentSpeed += 0.5
            self.ball['dy'] = self.currentSpeed
            self.ball['dx'] = -self.currentSpeed
            # print('Current speed:', self.currentSpeed)

        # Check for scoring
        if self.ball['x'] - self.ball['radius'] < 0 or self.ball['x'] + self.ball['radius'] > self.canvasWidth:
            self.currentSpeed = self.initialSpeed
            self.ball['dx'] = -self.currentSpeed
            self.ball['dy'] = self.currentSpeed

            if self.ball['x'] + self.ball['radius'] > self.canvasWidth:
                self.numberOfHitsP1 += 1
                # Set new speed and direction
            elif self.ball['x'] - self.ball['radius'] < 0:
                self.numberOfHitsP2 += 1

            # Reset ball position to center
            self.ball['x'] = self.canvasWidth/2

    def game_loop(self):
        if self.numberOfHitsP1 < 10 and self.numberOfHitsP2 < 10:
            self.update_game()
        else:
            if self.numberOfHitsP1 == 10:
                self.winner = 1
            elif self.numberOfHitsP2 == 10:
                self.winner = 2
            self.isGameExited = True
