<template>
  <div class="formTournament">
    <div class="player-bar">

      <!-- Toggle button -->
      <div v-if="ongoingTournament" class="name-container">
        <img src="https://picsum.photos/100" class="float-start picture" />
        <p v-if="ongoingTournament" class="player-name float-start"><strong>{{this.all_players[this.player_one].name}}</strong></p>
      </div>
      <button @click="toggleForm" class="start-tournament">
        {{ formVisible ? 'No Tournament' : 'Local Tournament' }}
      </button>
      <div v-if="ongoingTournament" class="name-container">
        <img src="https://picsum.photos/100" class="float-end picture" />
        <p v-if="ongoingTournament" class="player-name float-end"><strong>{{this.all_players[this.player_two].name}}</strong></p>
      </div>
    </div>

    <!-- Form (shown/hidden based on formVisible) -->
    <div v-if="formVisible" class="tournament-settings">
      <form>
        <label for="nbrPlayerRange" class="form-label">Number of total Players</label>
        <div class="mb-3 d-flex align-items-center">
          <input type="range" class="form-range" min="3" max="42" id="nbrPlayerRange" v-model.number="nbr_players" @input="updatePlayerCount">
          <input type="number" class="form-control" v-model.number="nbr_players" min="3" max="42" @input="updatePlayerCount">
        </div>
        <div class="name-box">
          <div v-for="index in nbr_players" :key="index" class="name-input">
            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
              <input
                type="radio"
                class="btn-check"
                :name="radioGroupName(index)"
                :id="'btnradio1' + index"
                autocomplete="off"
                checked
                @change="setActiveRadio('Player', index)"
              />
              <label class="btn btn-outline-primary" :for="'btnradio1' + index">Player</label>

              <input
                type="radio"
                class="btn-check"
                :name="radioGroupName(index)"
                :id="'btnradio2' + index"
                autocomplete="off"
                @change="setActiveRadio('Bot', index)"
              />
              <label class="btn btn-outline-primary" :for="'btnradio2' + index">Bot</label>
            </div>
            <input :id="'name' + index" type="text" class="form-input" :value="getPlayerValue(index)" @input="updatePlayerName(index, $event)">
          </div>
        </div>
        <button type="submit" @click="startTournament" class="start-tournament">Start Tournament</button>
      </form>
    </div>
  </div>
</template>

<script>
import LocalPong from './LocalPong.vue';

export default {
  data() {
    return {
      all_players: [],
      nbr_players: '3',
      formVisible: false,
      ongoingTournament: false,
      player_one: 0,
      player_two: 1,
    };
  },
  props: ['isGameWon'],
  computed: {
    // Computed property to generate unique radio button group names
    radioGroupName() {
      return (index) => `btnradio${index}`;
    },
  },
  methods: {
    toggleForm() {
      this.formVisible = !this.formVisible;
      console.log(this.formVisible)
      if (this.formVisible)
        this.updatePlayerCount();
      else
        this.all_players = [];
    },
    updatePlayerCount() {
      const currentCount = this.all_players.length;

      if (this.nbr_players > currentCount) {
        // Add new players to the array
        for (let i = currentCount + 1; i <= this.nbr_players; i++) {
          this.all_players.push({
            name: `Player-${i}`,
            games_won: '[]',
            player_or_bot: 'Player',
          });
        }
      } else if (this.nbr_players < currentCount) {
        // Remove players from the end of the array
        this.all_players.splice(this.nbr_players);
      }
    },
    startTournament() {
      console.log(this.all_players)
      this.updatePlayerName()
      this.formVisible = false;
      this.ongoingTournament = true;
      const total_games = 3;
      for (let games_played = 0; games_played < total_games; games_played++) {
          ;
        }
      }

      //logic
    },
    setActiveRadio(value, index) {
      this.all_players[index - 1].name = value + "-" + index;
      if (value == 'Bot') {
        this.all_players[index - 1].player_or_bot = 'Bot';
      }
      else
        this.all_players[index - 1].player_or_bot = 'Player';
    },
    updatePlayerName(index, event) {
      if (index >= 0 && index < this.all_players.length)
        this.all_players[index - 1].name = event.target.value;
    },
    getPlayerValue(index) {
      if (this.all_players[index - 1] !== undefined)
        return this.all_players[index - 1].name;
    }
  },
};
</script>

<style scoped>
	.start-tournament{
    display: flex;
    margin: 10px auto; /* Center the button horizontally */
    padding: 10px;
    font-size: 16px;
    height: 50px;
	}

  .player-bar {
    width: 800px;
    height: 110px;
    margin: auto;
    flex-direction: row;
    display: flex;
  }
  .name-container {
    width: 40%;
    overflow: hidden;
  }
  .tournament-settings {
    width: 800px;
    margin: auto;
  }


  .form-range {
    width: 650px;
  }

  .form-control {
    width: 100px;
    margin-left: 50px;
  }

  .name-box {
    display: flex;
    max-width: 800px;
    flex-wrap: wrap;
    justify-content: space-between; /* Align even elements to the right and odd elements to the left */
  }

  .name-input {
    max-width: 400px;
    margin: 5px;
  }
  .picture {
    width: 100px;
    height: 100px;
  }

  .player-name {
    margin: 10px;
    margin-top: 5px;
  }
</style>
