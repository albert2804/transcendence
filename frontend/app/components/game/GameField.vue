<template>
  <div
  	class="game-canvas" ref="gameFieldRef" tabindex="0" @touchstart="handleTouchPress" @touchend="handleTouchRelease" :style="map != '' ? { 'background-image': 'url(' + map + ')', 'background-repeat': 'no-repeat', 'background-position': 'center', 'background-size': '100% 100%' } : {}">
    <div v-show="playing" class="ball" :style="{ left: ballPos.x + '%', top: ballPos.y + '%', border: '1px solid black' }"></div>
	<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ffffff; font-size: 20vh; z-index: 2;" v-if="countdown > 0">
		{{ countdown }}
	</div>
    <div v-show="playing" class="paddle_1" :style="{ left: p1pos.x + 'px', top: p1pos.y + '%', height: paddleSize + '%', border: '2px solid black' }"></div>
    <div v-show="playing" class="paddle_2" :style="{ left: p2pos.x + '%', top: p2pos.y + '%', height: paddleSize + '%', border: '2px solid black' }"></div>
    <div v-show="playing" class="midline"></div>
    <div v-show="playing" style="position: absolute; top: 0; left: 2%; font-size: 1.2em; color: #ffffff; -webkit-text-stroke: 1px black;">
      {{ p1_name }}
    </div>
    <div v-show="playing" style="position: absolute; top: 0; right: 2%; font-size: 1.2em; color: #ffffff; -webkit-text-stroke: 1px black;">
      {{ p2_name }}
    </div>
    <div v-show="playing" style="position: absolute; bottom: 0; left: 2%; font-size: 2.0em; color: #ffffff; -webkit-text-stroke: 1px black;">
      {{ pointsP1 }}
    </div>
    <div v-show="playing" style="position: absolute; bottom: 0; right: 2%; font-size: 2.0em; color: #ffffff; -webkit-text-stroke: 1px black;">
      {{ pointsP2 }}
    </div>
    <div class="container nes-container is-rounded is-centered menu_box" v-if="!playing" >
        <!-- Message --->
        <div style="color: #000000; text-align: center;">
          <div>{{ message }}</div>
        </div>
        <!-- Checkbox --->
        <div v-if="showMenu || showAliasScreen2">
          <label for="checkbox" style="color: black;">
            <input type="checkbox" id="checkbox" v-model="isChecked" @change="changeMode"> Gravity Mode
          </label>
        </div>
        <!-- Menu buttons --->
        <div v-if="showMenu">
          <button type="button" class="nes-btn btn-primary" @click="startTrainingGame">Start Training Game</button>
        </div>
        <div v-if="showMenu && loginStatus == 1">
          <button type="button" class="nes-btn btn-primary" @click="startRankedGame" >Start Ranked Game</button>
        </div>
        <div v-if="showMenu">
          <button type="button" class="nes-btn btn-primary" @click="startLocalGame">Start Local Game</button>
        </div>
        <!-- play on this device - button --->
        <div v-if="!playOnThisDevice">
          <button type="button" class="nes-btn btn-primary" @click="changeDevice">Play on this device</button>
        </div>
        <!-- alias screen -->
        <div class= "nes-field" v-if="showAliasScreen || showAliasScreen2">
          <input type="text" class="form-control nes-input" v-model="alias" placeholder="Enter alias" maxlength="20"> 
        </div>
        <div v-if="showAliasScreen || showAliasScreen2" style="height: 8px;"></div>
        <div v-if="showAliasScreen">
          <button type="button" class="nes-btn btn-primary" @click="createGuestPlayer">Enter</button>
        </div>
        <div v-if="showAliasScreen2">
          <button type="button" class="nes-btn btn-primary" @click="createGuestPlayer2">Enter</button>
        </div>
        <div v-if="showAliasScreen && !showAliasScreen2">
          <div style="color: #000000; text-align: center;">
            <p><br>Or you can log in instead!</p>
          </div>
          <router-link to="/login" tag="button" class="nes-btn btn-primary" @click.native="$emit('closeModal')">Login</router-link>
        </div>
        <!-- Back to menu - button --->
        <div v-if="waiting || showAliasScreen2" style="height: 5px;"></div>
        <div v-if="waiting || showAliasScreen2">
          <button type="button" class="nes-btn btn-primary" @click="backToMenu">Back to Menu</button>
        </div>
        <div v-if="showMenu && loginStatus == 1">
          <button type="button" class="nes-btn btn-primary" @click="showControls">Controls</button>
          <div v-if="showControlsPic" style="position: relative; width: 100%;">
            <img v-if="controls" :src="controls" alt="Controls" style="width: 100%;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #000000; text-align: center;">
              <p>Press the arrow keys or 'w' and 's' to move the paddles!</p>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>
  
<script>
  import { isLoggedIn, sound } from '~/store';
  import { gameButtonState } from '~/store';
  export default {
  name: 'GameField',
  data () {
    return {
      loginStatus: isLoggedIn,
      socket: null,
      message: '',
      pointsP1: 0,
      pointsP2: 0,
      waiting: false,
      playing: false,
      showMenu: false,
      p1_name: '',
      p2_name: '',
	    countdown: 0,
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
      intersection: false,
		  playOnThisDevice: true,
      // Following only for guest users:
      showAliasScreen: false,
      showAliasScreen2: false,
      alias: '',
      controls: '',
      showControlsPic: false,
      map: '',
      isChecked: false,
      mode: 'default',
      playlist: [
        "endpoint/media/sounds/background.mp3",
        "endpoint/media/sounds/background2.mp3",
        "endpoint/media/sounds/background3.mp3",
        "endpoint/media/sounds/background4.mp3",
        "endpoint/media/sounds/background5.mp3",
        "endpoint/media/sounds/background6.mp3",
      ]

    }
  },
  watch: {
    isLoggedIn: {
      immediate: true,
      handler(newValue) {
		    this.loginStatus = newValue;
      }
    }
  },
  mounted () {
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
  expose: ['giveUpGame', 'handleKeyPress', 'handleKeyRelease'],
  methods: {
    // function to create and handle the websocket
	  createWebSocket () {
      const currentDomain = window.location.hostname;
      const sockurl = 'wss://' + currentDomain + '/endpoint/remoteGame/';
      this.socket = new WebSocket(sockurl)
      // create sound effects
      const intersection = new Audio("endpoint/media/sounds/ball.mp3");
      const randomNumber = Math.floor(Math.random() * 6); 
      console.log(randomNumber);
      const background = new Audio(this.playlist[randomNumber]);
      // const background = new Audio("endpoint/media/sounds/background.mp3");
      const effects = [intersection, background];
      this.socket.onopen = () => {
		    gameButtonState.value = "loading";
      }

      this.socket.onclose = () => {
        gameButtonState.value = "disconnected";
        this.$emit('closeModal');
      }

      this.socket.onerror = (error) => {
        gameButtonState.value = "disconnected";
        this.$emit('closeModal');
      }

      this.socket.onmessage = (event) => {
        try {
          // console.log('Received WebSocket message:', event.data);
          const data = JSON.parse(event.data);
          if (data.type === "redirect") {
            this.countdown = 0;
			      gameButtonState.value = "connected";
            this.showAliasScreen = false;
            this.showAliasScreen2 = false;
            if (data.page === "playing") {
              if (this.loginStatus == 1) {
                this.fetch_map();
              };
              this.message = '';
              this.waiting = false;
              this.playing = true;
              this.showMenu = false;
			  this.p1pos.y = (100 - this.paddleSize) / 2;
			  this.p2pos.y = (100 - this.paddleSize) / 2;
			  this.ballPos.x = 49.25;
			  this.ballPos.y = 48.5;
            } else if (data.page === "waiting") {
              this.message = 'Waiting for opponent...';
              this.waiting = true;
              this.playing = false;
              this.showMenu = false;
            } else if (data.page === "menu") {
              this.message = '';
			        this.map = '';
              this.waiting = false;
              this.playing = false;
              this.showMenu = true;
            } else if (data.page === "other_device") {
              this.message = 'You are connected with another device!';
              this.waiting = false;
              this.playing = false;
              this.showMenu = false;
			        this.playOnThisDevice = false;
            } else if (data.page === "alias_screen" || data.page === "alias_screen_2") {
              this.waiting = false;
              this.playing = false;
              this.showMenu = false;
              this.alias = '';
              if (data.page === "alias_screen") {
                this.message = 'Hello guest, please enter your alias!';
                this.showAliasScreen = true;
                this.showAliasScreen2 = false;
              } else if (data.page === "alias_screen_2") {
                this.message = 'Please enter an alias for the second player!';
                this.showAliasScreen = false;
                this.showAliasScreen2 = true;
              }
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
            effects[1].pause();
            
          } else if (data.type === "player_names") {
            this.p1_name = data.p1_name;
            this.p2_name = data.p2_name;
          } else if (data.type === 'game_update') {
            const gameState = data.state;
            const highScore = data.high_score;
            this.pointsP1 = highScore.pointsP1;
            this.pointsP2 = highScore.pointsP2;
            this.updateGameUI(gameState,effects);
          } else if (data.type === "alias_exists") {
            this.message = "Alias already taken!";
          } else if (data.type === "open_game_modal") {
            this.$emit('openModal');
          } else if (data.type === "close_game_modal") {
			      this.$emit('closeModal');
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
        this.map='';
        this.socket.close()
        // console.log('WebSocket connection closed')
      }
    },
    // function to fetch the map from the server
    async fetch_map(){
      try {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/user/info/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          }
        })
        if (response.ok) {
          const data = await response.json();
          this.map = data.map;
          console.log(this.map)
        }
      } catch (error) {
          this.map = '';
      }
    },
    // function to start a training game
    startTrainingGame () {

      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_training_game',
          alias: this.alias,
          mode: this.mode,
        });
        console.log(this.mode);
        this.socket.send(data);
      }
    },
    // function to start a local game
    startLocalGame () {

      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_local_game',
          mode: this.mode,
        });
        console.log(this.mode);
        this.socket.send(data);
      }
    },
    // function to start a ranked game
    startRankedGame () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'start_ranked_game',
          mode: this.mode,
        });
        console.log(this.mode);
        this.socket.send(data);
      }
    },
    // function to create a guest player (send alias to server)
    createGuestPlayer () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'create_guest_player',
          alias: this.alias,
          mode: this.mode,
        });
        this.socket.send(data);
      }
    },
    // create second guest player
    createGuestPlayer2 () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({
          type: 'create_guest_player_2',
          alias: this.alias,
          mode: this.mode,
        });
        this.socket.send(data);
      }
    },
    // go back to the menu
    backToMenu () {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'back_to_menu' });
        this.socket.send(data);
      }
    },
    // handler for key press
    handleKeyPress(event){
      if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's') {
        if (this.pressedKeys.includes(event.key)) {
          return;
        }
        this.pressedKeys.push(event.key);
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
          const data = JSON.stringify({ type: 'key_pressed', key: event.key });
          this.socket.send(data);
        }
      }
	// P for pause
	  if (event.key === 'p' || event.key === 'P') {
		if (this.socket && this.socket.readyState === WebSocket.OPEN) {
		  const data = JSON.stringify({ type: 'pause' });
		  this.socket.send(data);
		}
	  }
    },
    // handler for key release
    handleKeyRelease(event){
      if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's') {
        this.pressedKeys = this.pressedKeys.filter(key => key !== event.key);
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
          const data = JSON.stringify({ type: 'key_released', key: event.key });
          this.socket.send(data);
        }
      }
    },
    // handler for touch press (mobile)
    handleTouchPress(event) {
      const rect = this.$refs.gameFieldRef.getBoundingClientRect();
      const fieldHeight = rect.height;
      const fieldWidth = rect.width;
      let key;
      // iterate over all touches
      // (multi-touch possibility because of the local multiplayer mode)
      for (let i = 0; i < event.touches.length; i++) {
        const touch = event.touches[i];
        // get X and Y coordinates of the touch (relative to the game field)
        const touchY = touch.clientY - rect.top;
        const touchX = touch.clientX - rect.left;
        if (touchX < fieldWidth / 2) {
          if (touchY < fieldHeight / 2) {
            key = 'w';
          } else {
            key = 's';
          }
        } else {
          if (touchY < fieldHeight / 2) {
            key = 'ArrowUp';
          } else {
            key = 'ArrowDown';
          }
        }
        this.handleKeyPress({ key: key });
      }
    },
    // handler for touch release (mobile)
    handleTouchRelease(event) {
      // event.changedTouches is a list of all touches that changed in this event
      // it's nearly impossible to release two keys at the same time, so we only need [0] ;)
      const rect = this.$refs.gameFieldRef.getBoundingClientRect();
      const fieldWidth = rect.width;
      const touch = event.changedTouches[0];
      const mouseX = touch.clientX - rect.left;
      let keyUp, keyDown;
      if (mouseX < fieldWidth / 2) {
        keyUp = 'w';
        keyDown = 's';
      } else {
        keyUp = 'ArrowUp';
        keyDown = 'ArrowDown';
      }
      this.handleKeyRelease({ key: keyUp });
      this.handleKeyRelease({ key: keyDown });
    },
    // function to update the game UI (called when receiving game state from server)
    updateGameUI(gameState, effects) {
      if (sound.value)
        effects[1].play();
      this.p1pos.y = gameState.leftPaddle.y;
      this.p2pos.y = gameState.rightPaddle.y;
      this.ballPos.x = gameState.ball.x - (1.5/2); // 1.5% is the width of the ball
      this.ballPos.y = gameState.ball.y - (3/2);   // 3% is the height of the ball
      this.countdown = gameState.countdown;
      
    },
    // function to send information to server that the user wants to play on this device
    changeDevice() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const data = JSON.stringify({ type: 'change_device' });
      this.socket.send(data);
      }
      this.playOnThisDevice = true;
    },
    // give up the game
    giveUpGame() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const data = JSON.stringify({ type: 'give_up' });
        this.socket.send(data);
      }
    },
    // show controls in form of a gif
    async showControls() {
      this.showControlsPic=true;
      this.controls='https://media.tenor.com/Ycl8mXFNE_8AAAAi/get-real-cat.gif';
      await new Promise(resolve => setTimeout(resolve, 3000));
      this.showControlsPic=false;
    },
    
    changeMode () {
      if (!this.isChecked)
        this.mode = 'default';
      else
        this.mode = 'gravity';
      console.log(this.mode);
    },
  }
};
</script>

<!-- Styles -->
<style scoped>

.game-canvas {
  width: 100%;
  height: 97vh;
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
    z-index: 1;
    width: 2px;
    height: 100%;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #fff;
}

.ball {
  position: absolute;
  z-index: 1;
  width: 1.5%;
  height: 3%;
  background-color: rgb(255, 255, 255);
  border-radius: 50%;
}

.btn-primary{
  width: 97%;
}

.menu_box{
  min-width: 280px;
  max-width: 25vw;
  color: #ffffff;
  background-color: #eeeeee;
  display: inline-block;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.0em;
}

.menu_box * {
  font-size: inherit;
}

@media screen and (max-width: 800px) {
  .menu_box {
    font-size: 0.7em; 
  }
}

</style>