<!--
  This component displays a local pong game, setting the initial canvas size to
  800 x 400
-->

<template>
	<div>
		<div class="score-container">{{ numberOfWinsP1 }} : {{ numberOfWinsP2 }}</div>
		<div style="display: flex;">	
			<button @click="startGame" class="start-button">Start Game</button>
			<!-- <button @click="startTournament" class="start-tournament">Start Tournament</button> -->
		</div>
	  <canvas ref="pongCanvas" width="800" height="400"></canvas>
	</div>
</template>
  
  <script>
  export default {
		name: 'LocalPong',
	data() {
		const canvasHeight = 400;
		const canvasWidth = 800;
	  return {
		canvas: null,
		context: null,
		initialSpeed: 3,
		currentSpeed: 3,
		numberOfWinsP1: 0,
		numberOfWinsP2: 0,
		canvasWidth: canvasWidth,
		canvasHeight: canvasHeight,
		isGamePaused: false,
		isGameExited: false,
		leftPaddle: {
		  x: 0,
		  y: 160,
		  width: 10,
		  height: 80,
		  dy: 0,
		},
		rightPaddle: {
		  x: 790,
		  y: 160,
		  width: 10,
		  height: 80,
		  dy: 0,
		},
		ball: {
		  x: 400,
		  y: 200,
		  radius: 6,
		  dx: 0,
		  dy: 0,
		},
	  };
	},
	mounted() {
	  this.canvas = this.$refs.pongCanvas;
	  this.context = this.canvas.getContext('2d');
	  this.setupGame();
	  this.handleKeyDown = this.handleKeyDown.bind(this);
	  this.handleKeyUp = this.handleKeyUp.bind(this);
	  window.addEventListener('keydown', this.handleKeyDown);
	  window.addEventListener('keyup', this.handleKeyUp);
	},
	methods: {
	
	  setupGame() {
		this.draw();
		},
		
	  startGame() {
        this.resetGame();
		this.gameLoop();
      },

	  drawPaddle(x, y, width, height) {
		this.context.fillStyle = 'white';
		this.context.fillRect(x, y, width, height);
	  },

	  drawBall(x, y, radius) {
		this.context.beginPath();
		this.context.arc(x, y, radius, 0, Math.PI * 2, false);
		this.context.fillStyle = 'pink';
		this.context.fill();
		this.context.closePath();
	  },

	  updateGame() {
		// if game is paused, game will not be updated
		if (this.isGamePaused) {
			return;
		}
		//update paddle position
		this.leftPaddle.y += this.leftPaddle.dy;
		this.rightPaddle.y += this.rightPaddle.dy;
		
		// ensure paddles stay within canvas
		this.leftPaddle.y = Math.max(0, Math.min(this.canvasHeight - this.leftPaddle.height, this.leftPaddle.y));
		this.rightPaddle.y = Math.max(0, Math.min(this.canvasHeight - this.rightPaddle.height, this.rightPaddle.y));
  
		// move ball
		this.ball.x += this.ball.dx;
		this.ball.y += this.ball.dy;
  
		// bounce off top or bottom of canvas
		if (this.ball.y - this.ball.radius < 0 || this.ball.y + this.ball.radius > this.canvasHeight) {
		  this.ball.dy = -this.ball.dy;
		}
		
		// bounce off paddles and increase ball speed
		if (
		  this.ball.x - this.ball.radius < this.leftPaddle.x + this.leftPaddle.width &&
		  this.ball.y > this.leftPaddle.y && this.ball.y < this.leftPaddle.y + this.leftPaddle.height
		) {
			this.currentSpeed += 1;
			this.ball.dy = -this.currentSpeed;
			this.ball.dx = this.currentSpeed;
		  	console.log('current speed:', this.currentSpeed);
		}
  
		if (
		  this.ball.x + this.ball.radius > this.rightPaddle.x &&
		  this.ball.y > this.rightPaddle.y && this.ball.y < this.rightPaddle.y + this.rightPaddle.height
		) {
			this.currentSpeed += 1;
			this.ball.dy = this.currentSpeed;
			this.ball.dx = -this.currentSpeed;
		  	console.log('current speed:', this.currentSpeed);
		}
		// check for scoring
		if (this.ball.x - this.ball.radius < 0 || this.ball.x + this.ball.radius > this.canvasWidth) {
		  if (this.ball.x + this.ball.radius > this.canvasWidth) {
			  this.numberOfWinsP1 += 1;
			  // set new speed and direction
			  this.currentSpeed = this.initialSpeed;
			  this.ball.dx = -this.currentSpeed;
			  this.ball.dy = this.currentSpeed;
			  console.log('score player 1:', this.numberOfWinsP1);
		  }  
		  else if (this.ball.x - this.ball.radius < 0){
			  this.numberOfWinsP2 += 1;
			  // set new speed and direction
			  this.currentSpeed = this.initialSpeed;
			  this.ball.dx = this.currentSpeed;
			  this.ball.dy = this.currentSpeed;
			  console.log('score player 2:', this.numberOfWinsP2);
		  }
		  // reset ball position to center	
		  this.ball.x = this.canvasWidth/2;
		  this.ball.y = this.canvasHeight/2;
		}
	  },

	  draw() {
		this.context.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
  
		this.drawPaddle(this.leftPaddle.x, this.leftPaddle.y, this.leftPaddle.width, this.leftPaddle.height);
		this.drawPaddle(this.rightPaddle.x, this.rightPaddle.y, this.rightPaddle.width, this.rightPaddle.height);
  
		this.drawBall(this.ball.x, this.ball.y, this.ball.radius);
  
		this.context.beginPath();
		this.context.setLineDash([5, 5]);
		this.context.moveTo(this.canvasWidth/2, 0);
		this.context.lineTo(this.canvasWidth/2, this.canvasHeight);
		this.context.strokeStyle = 'white';
		this.context.stroke();
		this.context.closePath();
		this.context.setLineDash([]);
	  },

	  exitGame() {
		console.log('Exiting the game');
		this.isGameExited = true;
	  },

	  resetGame() {
		// Reset parameters
		this.numberOfWinsP1 = 0;
		this.numberOfWinsP2 = 0;
		this.isGameExited = false;
		this.isGamePaused = false;

		// Reset paddles
		this.leftPaddle.x = 0;
    	this.leftPaddle.y = this.canvasHeight/2 - this.leftPaddle.height/2;
    	this.rightPaddle.x = this.canvasWidth - this.rightPaddle.width;
    	this.rightPaddle.y = this.canvasHeight/2 - this.rightPaddle.height/2;

		// Reset ball
		this.ball.x = this.canvasWidth/2;
		this.ball.y = this.canvasHeight/2;
		this.ball.dx = this.initialSpeed;
		this.ball.dy = this.initialSpeed;

		// Reset speed values
		this.initialSpeed = 3;
		this.currentSpeed = 3;
		this.draw();
	  },
	  //main game loop
	  gameLoop() {
		// Check if escape button has been hit
		if (this.isGameExited == true) {
			this.resetGame();
		}
  		// Check if the maximum number of games has been reached
  		else if (this.numberOfWinsP1 < 10 && this.numberOfWinsP2 < 10) {
    	  this.updateGame();
    	  this.draw();
    	  requestAnimationFrame(() => this.gameLoop());
  	  	}
	  	else {
    	  console.log("Maximum number of games reached. Game loop stopped.");
		//   this.numberOfWinsP1 = 0;
		//   this.numberOfWinsP2 = 0;
  		}
	  },
	  handleKeyDown(e) {
		switch (e.key) {
		  case 'ArrowUp':
			this.rightPaddle.dy = -10;
			break;
		  case 'ArrowDown':
			this.rightPaddle.dy = 10;
			break;
		  case 'w':
			this.leftPaddle.dy = -10;
			break;
		  case 's':
			this.leftPaddle.dy = 10;
			break;
		  case 'p':
		  	this.isGamePaused = !this.isGamePaused;
			break;
		  case 'Escape':
			this.exitGame();
			break;
		}
	  },

	  // method to stop movement of handles when keys are released
	  handleKeyUp(e) {
		switch (e.key) {
		  case 'ArrowUp':
		  case 'ArrowDown':
			this.rightPaddle.dy = 0;
			break;
		  case 'w':
		  case 's':
			this.leftPaddle.dy = 0;
			break;
		}
	  },
	},
  };
  </script>
  
  <style scoped>
  .start-button {
	display: block;
    margin: 10px auto; /* Center the button horizontally */
    padding: 10px;
    font-size: 16px;
  }

  canvas {
	display: block;
	margin: auto;
	background-color: black;
  }

  .score-container {
	display: flex;
    justify-content: center; /* Center the content horizontally */
    align-items: flex-start; /* Align the content to the top */
    color: blue;
    font-size: 80px;
    margin-top: 50px; /* Adjust the margin-top value */
    position: absolute;
    top: 0; /* Position at the top */
    left: 0;
    right: 0;
    z-index: 1;
  }

  </style>
  