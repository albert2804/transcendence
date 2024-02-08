<template>
  <form>
    <label for="nbrPlayerRange" class="form-label">Number of total Players</label>
    <div class="mb-3 align-items-center position-relative">
      <input type="range" class="form-range" min="0" max="3" step="1" id="nbrPlayerRange" 
          v-model.number="selectPos" @input="updatePlayerCount">
      <h6 class="float-end" >{{ selectedData }}</h6>
    </div>
    <div class="name-box">
      <div v-for="index in nbr_players" :key="index" class="name-input">
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
          <input type="radio" class="btn-check" :name="radioGroupName(index)" :id="'btnradio1' + index"
                    autocomplete="off" checked @change="setActiveRadio('Player', index)"/>
          <label class="btn btn-outline-primary" :for="'btnradio1' + index">Player</label>
          <input type="radio" class="btn-check" :name="radioGroupName(index)"
                 :id="'btnradio2' + index" autocomplete="off" @change="setActiveRadio('Bot', index)"/>
          <label class="btn btn-outline-primary" :for="'btnradio2' + index">Bot</label>
        </div>
        <input :id="'name' + index" type="text" class="form-input" :value="getPlayerValue(index)" 
                @input="updatePlayerName(index, $event)">
      </div>
    </div>
    <button type="submit" @click="startTournament" class="start-tournament">Start Tournament</button>
  </form>
</template>


<script>

export default {
  name: 'FormTournament',
  data() {
    return {
      all_players: [],
      all_matches: [],
      tournamentSize: [4, 8, 16, 32],
      selectPos: 1,
      nbr_players: '8',
    };
  },
  computed: {

    selectedData() {
      this.nbr_players = this.tournamentSize[this.selectPos];
      return this.tournamentSize[this.selectPos];
    },

    //function to generate unique names for radio button
    radioGroupName() {
      return (index) => `btnradio${index}`;
    },
  },
  methods: {
    // ? i dont know why my index begins at 1
    setActiveRadio(value, index) {
      this.all_players[index - 1].name = value + "-" + index;
      if (value == 'Bot') {
        this.all_players[index - 1].player_or_bot = 'Bot';
      } else {
        this.all_players[index - 1].player_or_bot = 'Player';
      }
    },
    updatePlayerName(index, event) {
      if (index >= 0 && index <= this.all_players.length)
      this.all_players[index - 1].name = event.target.value;
    },

    getPlayerValue(index) {
      if (this.all_players[index - 1] != undefined)
        return this.all_players[index - 1].name;
    },

    // Pushes new Player Object into all_players list if the range/number 
    // of players is adjusted 
    updatePlayerCount () {
      const currentCount = this.all_players.length;

      if (this.nbr_players > currentCount) {
        for (let i = currentCount + 1; i <= this.nbr_players; i++) {
          this.all_players.push({
            name: `Player-${i}`,
            games_won: '[]',
            player_or_bot: 'Player',
            index: i - 1,
          });
        }
      } else if (this.nbr_players < currentCount) {
        // removes players from the all_pllayer list
        this.all_players.splice(this.nbr_players);
      }
    },

    startTournament() {
      //TODO: needs to call backend for tournament handling which is not yet implementet
      console.log("Tournament handling not yet implemented in backend");
    }
  },  
}
</script>