    <!-- need to think about when to create the websocket; probably when pressing the "start game" button -->

<!-- <template>
	<div>
	  <canvas ref="pongCanvas" width="800" height="400"></canvas>
	  <div class="score-container">{{ numberOfHitsP1 }} : {{ numberOfHitsP2 }}</div>
	</div>
  </template> -->

<template>
  	<div>
	  <canvas ref="pongCanvas" width="800" height="400"></canvas>
	  <div class="score-container">{{ numberOfHitsP1 }} : {{ numberOfHitsP2 }}</div>
	</div>
  <div
      class="game-canvas"
      tabindex="0"
      @keyup="handleKeyUp"
      @keydown="handleKeyDown"
  >
      <div class="paddle_1" :style="{ left: p1pos.x + 'px', top: p1pos.y + '%', height: paddleSize + '%' }"></div>
      <div class="paddle_2" :style="{ left: p2pos.x + '%', top: p2pos.y + '%', height: paddleSize + '%' }"></div>
      <!-- centered text -->
      <!-- <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.6em; font-weight: bold; color: #000; text-align: center;">
          <div v-if="message">{{ message }}</div>
      </div> -->
  </div>
  </template>
  
  <script>
  import { isLoggedIn } from '~/store';
  export default {
  name: 'RemotePong',
  data () {
      const canvasHeight = 400;
      const canvasWidth = 800;
      const canvas = null;
      const context = null;
    return {
      socket: null,
      canvasHeight : canvasHeight,
      canvasWidth : canvasWidth,
      numberOfHitsP1 : 0,
      numberOfHitsP2 : 0,
      own_id : null,
      //
      pressedKeys: [],
      paddleSize: 20,
      p1pos: {
        x: 0,
        y: (100 - this.paddleSize) / 2,
      },
      p2pos: {
        x: 98,
        y: (100 - this.paddleSize) / 2,
      },
    }
  },
  mounted () {
    // document.addEventListener('keydown', this.handleKeyDown);
    // document.addEventListener('keyup', this.handleKeyUp);
    // Use $nextTick to ensure the canvas is rendered before accessing it
    this.$nextTick(() => {
      this.canvas = this.$refs.pongCanvas;
      this.context = this.canvas.getContext('2d');
    });
    // watch for changes in isLoggedIn from store/index.js
    // watchEffect(() => {
    //   if (isLoggedIn.value === 1) {
    //     this.createWebSocket();
    //   } else if (isLoggedIn.value === 0) {
    //     this.closeWebSocket();
    //   }
    // });

    watchEffect(() => {
      if (isLoggedIn.value === 1) {
        this.createWebSocket();
      } else if (isLoggedIn.value === 0) {
        this.closeWebSocket();
      }
    });
  },
  methods: {
    /* ------------- Web sockets -----------------------------------------*/
	  createWebSocket () {
      const currentDomain = window.location.hostname;
      const sockurl = 'wss://' + currentDomain + '/endpoint/remoteGame/';
      this.socket = new WebSocket(sockurl)

      this.socket.onopen = () => {
        console.log('opened remoteGame websocket')
        this.$emit('connected')
      }

      this.socket.onclose = () => {
        console.log('closed remoteGame websocket')
        // document.removeEventListener('keydown', this.handleKeyDown);
        // document.removeEventListener('keyup', this.handleKeyUp);
      }

      this.socket.onerror = (error) => {
        console.error(`WebSocket-Error: ${error}`)
      }

      this.socket.onmessage = (event) => {
        try {
          // console.log('Message received:', event.data);
          const data = JSON.parse(event.data);
          if (data.type === 'game_update') {
            if (data.state) {
              const gameState = data.state;
              const highScore = data.high_score;
              this.numberOfHitsP1 = highScore.numberOfHitsP1;
              this.numberOfHitsP2 = highScore.numberOfHitsP2;

              this.updateGameUI(gameState);
            } else {
              console.error('Received game_state message with undefined data:', data);
            }
          } else {
            console.error('Received message of unknown type:', data);
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      }
    },
    closeWebSocket () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.close()
        console.log('WebSocket connection closed')
      }
    },
    /* ------------- Event handler ---------------------------------------*/
    handleKeyDown(event){
      if (this.pressedKeys.includes(event.key)) {
        return;
      }
      this.pressedKeys.push(event.key);
      console.log("key_pressed: " + event.key);
      const data = JSON.stringify({ type: 'key_pressed', key: event.key });
      this.socket.send(data);
    },
    handleKeyUp(event){
      this.pressedKeys = this.pressedKeys.filter(key => key !== event.key);
      console.log("key_released: " + event.key);
      const data = JSON.stringify({ type: 'key_released', key: event.key });
      this.socket.send(data);
    },

    /* ------------- Update UI -------------------------------------------*/
    updateGameUI(gameState) {
      this.context.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
      this.drawPaddle(gameState.leftPaddle.x, gameState.leftPaddle.y, gameState.leftPaddle.width, gameState.leftPaddle.height);
      this.drawPaddle(gameState.rightPaddle.x, gameState.rightPaddle.y, gameState.rightPaddle.width, gameState.rightPaddle.height);
      this.drawBall(gameState.ball.x, gameState.ball.y, gameState.ball.radius);
      this.drawLine();
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
    drawLine() {
      this.context.beginPath();
      this.context.setLineDash([5, 5]);
      this.context.moveTo(this.canvasWidth / 2, 0);
      this.context.lineTo(this.canvasWidth / 2, this.canvasHeight);
      this.context.strokeStyle = 'white';
      this.context.stroke();
      this.context.closePath();
      this.context.setLineDash([]);
    },
  }
};
  </script>

  <!-- Styles -->
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

  
  .game-canvas {
  width: 100%;
  padding-bottom: 50%;
  border: 3px solid #0b51b4;
  background-color: #000;
  position: relative;
  overflow: hidden;
}

.paddle_1 {
  width: 2%;
  background-color: rgb(255, 255, 255);
  position: absolute;
}

.paddle_2 {
  width: 2%;
  background-color: rgb(255, 255, 255);
  position: absolute;
}

  </style>
  