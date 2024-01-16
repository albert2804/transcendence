<template>
  <div
      class="game-canvas" tabindex="0" @keyup="handleKeyUp" @keydown="handleKeyDown">
      <div class="score-container">{{ numberOfHitsP1 }} : {{ numberOfHitsP2 }}</div>
      <div class="ball" :style="{ left: ballPos.x + '%', top: ballPos.y + '%' }"></div>
      <div class="paddle_1" :style="{ left: p1pos.x + 'px', top: p1pos.y + '%', height: paddleSize + '%' }"></div>
      <div class="paddle_2" :style="{ left: p2pos.x + '%', top: p2pos.y + '%', height: paddleSize + '%' }"></div>
      <div class="midline"></div>
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
    return {
      socket: null,
      numberOfHitsP1 : 0,
      numberOfHitsP2 : 0,
      //
      pressedKeys: [],
      paddleSize: 20,
      p1pos: {
        x: 0,
        y: (100 - this.paddleSize) / 2,
      },
      p2pos: {
        x: 98.5,
        y: (100 - this.paddleSize) / 2,
      },
      ballPos: {
        // middle position minus half the ball size
        x: 50 - (1.5/2),
        y: 50 - (3/2),
      },
    }
  },
  mounted () {
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
      // NEW RESPONSIIVE GAME UI:
      // update paddle positions
      // convert height px(400) to %(100)
      // in future calculate this in backend and send only % values
      this.p1pos.y = gameState.leftPaddle.y / 400 * 100;
      this.p2pos.y = gameState.rightPaddle.y / 400 * 100;
      // update ball position
      this.ballPos.x = (gameState.ball.x / 800 * 100) - (1.5/2);
      this.ballPos.y = (gameState.ball.y / 400 * 100) - (3/2);
    },
  }
};
  </script>

  <!-- Styles -->
  <style scoped>
  .score-container {
	display: flex;
    justify-content: center;
    align-items: flex-start;
    color: blue;
    font-size: 80px;
    margin-top: 50px;
    position: absolute;
    top: 0;
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
  width: 1.5%;
  background-color: rgb(255, 255, 255);
  position: absolute;
}

.paddle_2 {
  width: 1.5%;
  background-color: rgb(255, 255, 255);
  position: absolute;
}

.midline {
    position: absolute;
    width: 1px;
    height: 100%;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #fff;
}

.ball {
  position: absolute;
  width: 1.5%;
  height: 3%;
  background-color: pink;
  border-radius: 50%;
}

  </style>
  