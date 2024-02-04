<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
  <div
      @keydown="handleKeyPress"
      @keyup="handleKeyRelease"
      class="game-canvas" ref="gameFieldRef" tabindex="0" @touchstart="handleTouchPress" @touchend="handleTouchRelease">
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
        {{ pointsP1 }}
      </div>
      <div v-show="playing" style="position: absolute; bottom: 0; right: 2%; font-size: 2.0em; color: #ffffff;">
        {{ pointsP2 }}
      </div>
	  <li style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; position: absolute;">
		<!-- Message --->
		<div style="font-size: 1.6em; font-weight: bold; color: #ffffff; text-align: center;">
			<div>{{ message }}</div>
		</div>
		<!-- Start game - button --->
		<div v-if="showMenu">
			<button type="button" class="btn btn-primary" @click="startTrainingGame">Start Training Game</button>
		</div>
    <div v-if="showMenu" style="height: 5px;"></div>
    <div v-if="showMenu">
      <button type="button" class="btn btn-primary" @click="startLocalGame">Start Local Game</button>
    </div>
    <div v-if="showMenu && isLoggedIn == 1" style="height: 5px;"></div>
    <div v-if="showMenu && isLoggedIn == 1">
      <button type="button" class="btn btn-primary" @click="startRankedGame">Start Ranked Game</button>
    </div>
		<!-- play on this device - button --->
		<div v-if="!playOnThisDevice">
			<button type="button" class="btn btn-primary" @click="changeDevice">Play on this device</button>
		</div>
    <!-- alias screen -->
    <div v-if="showAliasScreen">
      <input type="text" class="form-control" v-model="alias" placeholder="Enter alias" maxlength="20"> 
    </div>
    <div v-if="showAliasScreen" style="height: 5px;"></div>
    <div v-if="showAliasScreen">
      <button type="button" class="btn btn-primary" @click="create_guest_player">Enter</button>
    </div>
	</li>
  </div>
</template>
  
<script>
  import { isLoggedIn } from '~/store';
  export default {
  name: 'RemotePong',
  data () {
    return {
      socket: null,
      message: '',
      pointsP1: 0,
      pointsP2: 0,
      playing: false,
      showMenu: false,
      p1_name: '',
      p2_name: '',
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
        x: 0,
        y: 0,
      },
	    playOnThisDevice: true,
      // Following only for guest users:
      showAliasScreen: false,
      alias: '',
    }
  },
  mounted () {
    // watch for changes in the login status (need to close and reopen the websocket when the user logs in or out)
    watchEffect(() => {
      if (isLoggedIn.value === 1) {
        this.closeWebSocket();
        this.createWebSocket();
      } else if (isLoggedIn.value === 0) {
        this.closeWebSocket();
        this.createWebSocket();
      }
    });
  },
  beforeDestroy () {
    this.closeWebSocket();
  },
  methods: {
    // function to create and handle the websocket
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
          const data = JSON.parse(event.data);
          if (data.type === "redirect") {
            this.showAliasScreen = false;
            if (data.page === "playing") {
              this.message = '';
              this.playing = true;
              this.showMenu = false;
            } else if (data.page === "waiting") {
              this.message = 'Waiting for opponent...';
              this.playing = false;
              this.showMenu = false;
            } else if (data.page === "menu") {
              this.message = '';
              this.playing = false;
              this.showMenu = true;
            } else if (data.page === "other_device") {
              this.message = 'You are connected with another device!';
              this.playing = false;
              this.showMenu = false;
			        this.playOnThisDevice = false;
            } else if (data.page === "alias_screen") {
              this.message = 'hello guest, please enter your alias!';
              this.playing = false;
              this.showMenu = false;
              this.alias = '';
              this.showAliasScreen = true;
            }
          } else if (data.type === "game_result") {
            this.playing = false;
            this.showMenu = false;
            if (data.result === "winner") {
              this.message = "You won the game!";
            } else if (data.result === "loser") {
              this.message = "You lost the game!";
            } else if (data.result === "tied") {
              this.message = "Game finished without result!";
            } else if (data.result === "right") {
              this.message = "The right player won the game!";
            } else if (data.result === "left") {
              this.message = "The left player won the game!";
            }
          } else if (data.type === "player_names") {
            this.p1_name = data.p1_name;
            this.p2_name = data.p2_name;
          } else if (data.type === 'game_update') {
            const gameState = data.state;
            const highScore = data.high_score;
            this.pointsP1 = highScore.pointsP1;
            this.pointsP2 = highScore.pointsP2;
            this.updateGameUI(gameState);
          } else if (data.type === "alias_exists") {
            this.message = "Alias already taken!";
          } else {
            console.error('Received message of unknown type:', data);
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      }
    },
    // function to close the websocket
    closeWebSocket () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.close()
        console.log('WebSocket connection closed')
      }
    },
    // function to start the game
    startTrainingGame () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_training_game',
          alias: this.alias,
        });
        this.socket.send(data);
      }
    },
    // function to start a local game
    startLocalGame () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_local_game'
        });
        this.socket.send(data);
      }
    },
    startRankedGame () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_ranked_game'
        });
        this.socket.send(data);
      }
    },
    // function to create a guest player (send alias to server)
    create_guest_player () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'create_guest_player',
          alias: this.alias,
        });
        this.socket.send(data);
      }
    },
    // handler for key press
    handleKeyPress(event){
      if (this.pressedKeys.includes(event.key)) {
        return;
      }
      this.pressedKeys.push(event.key);
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'key_pressed', key: event.key });
        this.socket.send(data);
      }
    },
    // handler for key release
    handleKeyRelease(event){
      if (!this.pressedKeys.includes(event.key)) {
        return;
      }
      this.pressedKeys = this.pressedKeys.filter(key => key !== event.key);
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'key_released', key: event.key });
        this.socket.send(data);
      }
    },
    // handler for touch press (mobile)
    handleTouchPress(event) {
      const rect = this.$refs.gameFieldRef.getBoundingClientRect();
      const fieldHeight = rect.height;
      const touch = event.touches[0];
      const mouseY = touch.clientY - rect.top;

      if (mouseY < fieldHeight / 2) {
		event.key = 'ArrowUp';
		this.handleKeyPress(event);
      } else {
		event.key = 'ArrowDown';
		this.handleKeyPress(event);
      }
    },
    // handler for touch release (mobile)
    handleTouchRelease(event) {
		event.key = 'ArrowUp';
		this.handleKeyRelease(event);
		event.key = 'ArrowDown';
		this.handleKeyRelease(event);
    },
    // function to update the game UI (called when receiving game state from server)
    updateGameUI(gameState) {
      this.p1pos.y = gameState.leftPaddle.y;
      this.p2pos.y = gameState.rightPaddle.y;
      this.ballPos.x = gameState.ball.x - (1.5/2); // 1.5% is the width of the ball
      this.ballPos.y = gameState.ball.y - (3/2);   // 3% is the height of the ball
    },
    // function to send information to server that the user wants to play on this device
    changeDevice() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const data = JSON.stringify({ type: 'change_device' });
      this.socket.send(data);
      }
      this.playOnThisDevice = true;
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
  