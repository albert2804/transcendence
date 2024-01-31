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
        <div class="mb-3 align-items-center position-relative">
          <input type="range" class="form-range" min="0" max="3" step="1" id="nbrPlayerRange" v-model.number="selectPos" @input="updatePlayerCount">
          <!-- <input type="number" class="form-control" v-model.number="nbr_players" min="0" max="3" step="1" @input="updatePlayerCount"> -->
          <h6 class="float-end" >{{ selectedData }}</h6>
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
    <div v-if="ongoingTournament">
      <LocalTournamentBracket :numberOfPlayers="nbr_players" :matches="all_matches" />
    </div>
  </div>
</template>

<script>
import LocalTournamentBracket from './LocalTournamentBracket.vue';

export default {
  props: ['startGameTour', 'gameFinish', 'gameExited'],
  name: 'LocalTournament',
  data() {
    return {
      all_players: [],
      all_matches: [],
      nbr_players: '8',
      formVisible: false,
      ongoingTournament: false,
      player_one: 0,
      player_two: 1,
      isGameFinished: false,
      tournamentSize: [4, 8, 16, 32],
      selectPos: 1,
    };
  },
  computed: {
    selectedData() {
      this.nbr_players = this.tournamentSize[this.selectPos]
      return this.tournamentSize[this.selectPos]
    },
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

    async startTournament() {
      console.log(this.all_players)
      this.updatePlayerName()
      this.formVisible = false;
      this.ongoingTournament = true;

      console.log("nbr of players" + this.nbr_players);
      const total_games = this.nbr_players - 1; 
      console.log(total_games);
      console.log("start game")
      for (let match = 0; match < total_games; match++) {
        console.log(Math.log2(total_games) - Math.floor(Math.log2(match + 1)))
        this.all_matches.push({
          is_round: Math.floor(Math.log2(total_games + 1)) - Math.floor(Math.log2(total_games - match)),
          game_nbr: match + 1, 
          l_player: -1,
          r_player: -1,
          l_score: 0,
          r_score: 0,
        });
        if (this.all_matches[match].is_round == 1) {
          this.all_matches[match].l_player = this.all_players[match * 2];
          this.all_matches[match].r_player = this.all_players[match * 2 + 1];
        }
      }
      console.log(this.all_matches)
      const playGame = async () => {
        for (let match = 0; match < total_games; match++) {

          console.log("Before startGameTour");
          await this.startGameTour();
          console.log("After startGameTour, before waitForVariableChange");
          if (this.gameExited) {
            this.ongoingTournament = false;
            console.log("tournament exited")
            break;
          }
          await this.waitForVariableChange(() => this.gameFinish);
          console.log("After waitForVariableChange");
        }
      };
      playGame().then(() => {
        
        this.ongoingTournament = false;
        console.log("Tournament finished")
      });
    },

    async waitForVariableChange(conditionalCallback) {
      return new Promise((resolve) => {
        const checkCondition = () => {
          if (conditionalCallback()) {
            resolve();
          } else {
            setTimeout(checkCondition, 1);
          }
        };

        checkCondition();
      });
    },

      //logic
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
    },
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
    width: 700px;
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
