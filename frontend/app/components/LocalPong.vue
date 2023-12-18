<!--
  This component displays a local pong game, setting the initial canvas size to
  800 x 400
-->

<template>
	<div>
	  <div class="score-container">
		<div class="player-score">
		  Player 1: {{ numberOfWinsP1 }}
		</div>
		<div class="player-score">
		  Player 2: {{ numberOfWinsP2 }}
		</div>
	  </div>
	  <canvas ref="pongCanvas" width="800" height="400"></canvas>
	</div>
  </template>
  
  <script>
  export default {
	data() {
	  return {
		canvas: null,
		context: null,
		initialSpeed: 3,
		currentSpeed: 3,
		numberOfWinsP1: 0,
		numberOfWinsP2: 0,
		canvasWidth: 800,
		canvasHeight: 400,
		paddleWidth: 10,
		paddleHeight: 80,
		leftPaddle: {
		  x: 0,
		  y: 160,
		  width: 10,
		  height: 80,
		  dy: 7,
		},
		rightPaddle: {
		  x: 790,
		  y: 160,
		  width: 10,
		  height: 80,
		  dy: 7,
		},
		ball: {
		  x: 400,
		  y: 200,
		  radius: 6,
		  dx: 5,
		  dy: 5,
		},
	  };
	},
	mounted() {
	  this.canvas = this.$refs.pongCanvas;
	  this.context = this.canvas.getContext('2d');
	  this.setupGame();
	},
	methods: {
	  setupGame() {
		this.handleKeyDown = this.handleKeyDown.bind(this);
		this.handleKeyUp = this.handleKeyUp.bind(this);
		window.addEventListener('keydown', this.handleKeyDown);
		window.addEventListener('keyup', this.handleKeyUp);
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
		//update paddle position
		this.leftPaddle.y += this.leftPaddle.dy;
		this.rightPaddle.y += this.rightPaddle.dy;
		
		// ensure paddles stay within canvas
		this.leftPaddle.y = Math.max(0, Math.min(400 - this.leftPaddle.height, this.leftPaddle.y));
		this.rightPaddle.y = Math.max(0, Math.min(400 - this.rightPaddle.height, this.rightPaddle.y));
  
		// move ball
		this.ball.x += this.ball.dx;
		this.ball.y += this.ball.dy;
  
		// bounce off top or bottom of canvas
		if (this.ball.y - this.ball.radius < 0 || this.ball.y + this.ball.radius > 400) {
		  this.ball.dy = -this.ball.dy;
		}
		
		// bounce off paddles
		if (
		  this.ball.x - this.ball.radius < this.leftPaddle.x + this.leftPaddle.width &&
		  this.ball.y > this.leftPaddle.y &&
		  this.ball.y < this.leftPaddle.y + this.leftPaddle.height
		) {
		  this.ball.dx = -this.ball.dx;
		}
  
		if (
		  this.ball.x + this.ball.radius > this.rightPaddle.x &&
		  this.ball.y > this.rightPaddle.y &&
		  this.ball.y < this.rightPaddle.y + this.rightPaddle.height
		) {
		  this.ball.dx = -this.ball.dx;
		}
		// check for scoring
		if (this.ball.x - this.ball.radius < 0 || this.ball.x + this.ball.radius > 800) {
		  if (this.ball.x + this.ball.radius > 800) {
			  this.numberOfWinsP1 += 1;
			  console.log('score player 1:', this.numberOfWinsP1);
		  }  
		  else if (this.ball.x - this.ball.radius < 0){
			  this.numberOfWinsP2 += 1;
			  console.log('score player 2:', this.numberOfWinsP2);
		  }
		  // reset ball position	
		  this.ball.x = 400;
		  this.ball.y = 200;
  
		  this.currentSpeed += 1;
		  this.numberOfGames +=1;
		  if (this.currentSpeed > this.initialSpeed + 3) {
			//reset speed to inital speed after reaching a certain threshold
			this.currentSpeed = this.initialSpeed;
		  }
		  // set new speed
		  this.ball.dx = this.currentSpeed;
		  this.ball.dy = this.currentSpeed;
		}
	  },
	  draw() {
		this.context.clearRect(0, 0, 800, 400);
  
		this.drawPaddle(this.leftPaddle.x, this.leftPaddle.y, this.leftPaddle.width, this.leftPaddle.height);
		this.drawPaddle(this.rightPaddle.x, this.rightPaddle.y, this.rightPaddle.width, this.rightPaddle.height);
  
		this.drawBall(this.ball.x, this.ball.y, this.ball.radius);
  
		this.context.beginPath();
		this.context.setLineDash([5, 5]);
		this.context.moveTo(400, 0);
		this.context.lineTo(400, 400);
		this.context.strokeStyle = 'white';
		this.context.stroke();
		this.context.closePath();
  
		this.context.setLineDash([]);
	  },
	  //main game loop
	  gameLoop() {
  		// Check if the maximum number of games has been reached
  		if (this.numberOfWinsP1 < 10 && this.numberOfWinsP2 < 10) {
    	  this.updateGame();
    	  this.draw();
    	  requestAnimationFrame(() => this.gameLoop());
  	  	}
	  	else {
    	  console.log("Maximum number of games reached. Game loop stopped.");
		  this.numberOfWinsP1 = 0;
		  this.numberOfWinsP2 = 0;
  		}
	  },
	  handleKeyDown(e) {
		switch (e.key) {
		  case 'ArrowUp':
			this.rightPaddle.dy = -5;
			break;
		  case 'ArrowDown':
			this.rightPaddle.dy = 5;
			break;
		  case 'w':
			this.leftPaddle.dy = -5;
			break;
		  case 's':
			this.leftPaddle.dy = 5;
			break;
		}
	  },
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
  canvas {
	display: block;
	margin: auto;
	background-color: black;
  }
  .score-container {
    display: flex;
    justify-content: space-between;
    color: blue;
    font-size: 18px;
    margin-top: 10px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1;
  }

  .player-score {
    flex: 1;
    text-align: center;
  }
  </style>
  