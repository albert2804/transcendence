<template>
	<div>
	  <button @click="sendMessage" class="start-button">Start Game</button>
	  <!-- <button @click="startGame" class="start-button">Start Game</button> -->
	  <canvas ref="pongCanvas" width="800" height="400"></canvas>
	  <!-- <div class="score-container">{{ numberOfWinsP1 }} : {{ numberOfWinsP2 }}</div> -->
    <!-- <div @keydown="handleKeyDown" tabindex="0"></div> -->
	</div>
  </template>
  
  <script>
  import { isLoggedIn } from '~/store';
  export default {
  name: 'RemotePong',

  data () {
    return {
      socket: null,
      ball: {
        x: 400,
        y: 200,
        radius: 6,
        dx: 0,
        dy: 0,
		},
      // messages: [],
      // unseen: 0,
      // showScrollButton: false,
      // scrollEventListenerAdded: false,
      // newMessage: '',
    //   chatid: null,
    }
  },
  mounted () {
    this.createWebSocket();
    document.addEventListener('keydown', this.handleKeyDown);
    // watch for changes in isLoggedIn from store/index.js
    // watchEffect(() => {
    //   if (isLoggedIn.value === 1) {
    //     this.createWebSocket();
    //   } else if (isLoggedIn.value === 0) {
    //     this.closeWebSocket();
    //   }
    // });
  },
  methods: {
    updateGameUI(gameState) {
      this.ball.x = gameState.ball_x;
      this.ball.y = gameState.ball_y;
      console.log('updated ball_y', this.ball.y);

    },

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
        document.removeEventListener('keydown', this.handleKeyDown);
      }

      this.socket.onerror = (error) => {
        console.error(`WebSocket-Error: ${error}`)
      }

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

        if (data.type === 'game_state') {
          if (data.state) {
            const gameState = data.state;
            const ballXValue = gameState.ball_x;
            this.updateGameUI(gameState);
            console.log('ball_x value is:', ballXValue);

            // Now you can work with the ball_x value
            // For example, you can use it in other parts of your Vue component
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
      if (this.socket) {
        this.socket.close()
      }
    //   this.messages = []
    //   if (this.$el.querySelector('.chat-messages')) {
    //     this.$el.querySelector('.chat-messages').removeEventListener('scroll', this.checkScroll)
    //   }
    },

    // Method to handle keydown event and send the pressed key to the backend
    handleKeyDown(event) {
      const pressedKey = event.key;
      // Send the pressed key to the backend using your WebSocket connection
      this.sendKeyPressed(pressedKey);
    },

    // Method to send the pressed key to the backend
    sendKeyPressed(key) {
      // Use your WebSocket connection to send the key to the backend
      const data = { 'key_pressed': key};
      this.socket.send(JSON.stringify(data));
      console.log('key pressed:', key);
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
      }
    }
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
  