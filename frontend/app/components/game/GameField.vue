<template>
  <div
      class="game-canvas" ref="gameFieldRef" tabindex="0" @touchstart="handleTouchPress" @touchend="handleTouchRelease">
      <!-- <div class="score-container">{{ numberOfHitsP1 }} : {{ numberOfHitsP2 }}</div> -->
      <div v-show="playing" class="ball" :style="{ left: ballPos.x + '%', top: ballPos.y + '%' }"></div>
      <div v-show="playing" class="paddle_1" :style="{ left: p1pos.x + 'px', top: p1pos.y + '%', height: paddleSize + '%' }"></div>
      <div v-show="playing" class="paddle_2" :style="{ left: p2pos.x + '%', top: p2pos.y + '%', height: paddleSize + '%' }"></div>
      <div v-show="playing" class="midline"></div>
      <div v-show="playing" style="position: absolute; top: 0; left: 2%; font-size: 1.2em; color: #ffffff;">
        {{ p1_name }}
      </div>
      <div v-show="playing" style="position: absolute; top: 0; right: 2%; font-size: 1.2em; color: #ffffff;">
        {{ p2_name }}
      </div>
      <div v-show="playing" style="position: absolute; bottom: 0; left: 2%; font-size: 2.0em; color: #ffffff;">
        {{ numberOfHitsP1 }}
      </div>
      <div v-show="playing" style="position: absolute; bottom: 0; right: 2%; font-size: 2.0em; color: #ffffff;">
        {{ numberOfHitsP2 }}
      </div>
      <!-- centered text -->
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.6em; font-weight: bold; color: #ffffff; text-align: center;">
          <div v-if="message">{{ message }}</div>
      </div>
      <!-- centered Bootstrap button -->
      <div v-if="showMenu" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
        <button type="button" class="btn btn-primary" @click="startGame">Start Game</button>
      </div>
  </div>
</template>
  
<script>
  import { isLoggedIn } from '~/store';
  export default {
  name: 'RemotePong',
  data () {
    return {
      message: '',
      socket: null,
      //
      numberOfHitsP1: 0,
      numberOfHitsP2: 0,
      //
      playing: false,
      showMenu: false,
      p1_name: 'player 1', // left players name
      p2_name: 'player 2', // right players name
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
  beforeDestroy () {
    this.closeWebSocket();
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
          } else if (data.type === 'message') {
            this.message = data.message;
            // this.menu = false; // hide menu if you get already connected message and menu is still visible because you were connected as another user before
          } else if (data.type === "state") {
            // console.log('Received state message:', data);
            this.p1_name = data.p1_name;
            this.p2_name = data.p2_name;
            if (data.state === "playing") {
              this.message = '';
              this.playing = true;
              this.showMenu = false;
            } else if (data.state === "waiting") {
              this.message = 'Waiting for opponent...';
              this.playing = false;
              this.showMenu = false;
            } else if (data.state === "finished") {
              this.message = 'Game finished!';
              this.playing = false;
              this.showMenu = false;
            } else if (data.state === "menu") {
              this.message = '';
              this.playing = false;
              this.showMenu = true;
            } else if (data.state === "other_device") {
              // console.log('Received state message:', data);
              this.message = 'You are connected with another device!';
              this.playing = false;
              this.showMenu = false;
            } else {
              console.error('Received message of unknown type:', data);
            }
          } else if (data.type === "winner") {
            this.message = "You won the game!";
            this.playing = false;
            this.showMenu = false;
          } else if (data.type === "loser") {
            this.message = "You lost the game!";
            this.playing = false;
            this.showMenu = false;
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
    // function to send info to backend to start game (join waiting room)
    startGame () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'start_game' });
        this.socket.send(data);
      }
    },
    /* ------------- Event handler ---------------------------------------*/
    pressKey(keyToPress) {
      if (this.pressedKeys.includes(keyToPress)) {
        return;
      }
      this.pressedKeys.push(keyToPress);
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'key_pressed', key: keyToPress });
        this.socket.send(data);
      }
    },
    removeKey(keyToRemove) {
      if (!this.pressedKeys.includes(keyToRemove)) {
        return;
      }
      this.pressedKeys = this.pressedKeys.filter(key => key !== keyToRemove);
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'key_released', key: keyToRemove });
        this.socket.send(data);
      }
    },
    // handle keyboard events
    handleKeyDown(event){
      this.pressKey(event.key);
    },
    handleKeyUp(event){
      this.removeKey(event.key);
    },
    // handle touch events (mobile)
    handleTouchPress(event) {
      const rect = this.$refs.gameFieldRef.getBoundingClientRect();
      const fieldHeight = rect.height;
      const touch = event.touches[0];
      const mouseY = touch.clientY - rect.top;

      if (mouseY < fieldHeight / 2) {
        if (!this.pressedKeys.includes('ArrowUp')) {
          this.removeKey('ArrowDown');
          this.pressKey('ArrowUp');
        }
      } else {
        if (!this.pressedKeys.includes('ArrowDown')) {
          this.removeKey('ArrowUp');
          this.pressKey('ArrowDown');
        }
      }
    },
    handleTouchRelease(event) {
      this.removeKey('ArrowUp');
      this.removeKey('ArrowDown');
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
  