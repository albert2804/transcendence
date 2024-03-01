<template>
  <form style="max-width: 800px; margin: auto; overflow: hidden;">
    <div>
      <input type="text" placeholder="Tournament Name" @input="setTournamentName($event)"/>
    </div>
    <div class="mb-3">
      <label for="nbrPlayerRange" class="form-label">Number of Total Players</label>
      <div class="d-flex align-items-center">
        <input style="width: 80%; " type="range" class="form-range" min="0" max="3" step="1" id="nbrPlayerRange" 
          v-model.number="selectPos" @input="updatePlayerCount">
        <h6 style="rotate:90deg;" class="ms-3">{{ selectedData }}</h6>
      </div>
    </div>

    <div style="margin-bottom: 3%;" class="name-box row flex-wrap">
      <div v-for="index in nbr_players" style="min-width: 50%; margin-bottom: 1%" :key="index" class="name-input d-flex col-12 col-lg-1">
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
          <input type="radio" class="btn-check" :name="radioGroupName(index)" :id="'btnradio1' + index"
            autocomplete="off" checked @change="setActiveRadio('Player', index)"/>
          <label class="btn btn-outline-primary" :for="'btnradio1' + index">Player</label>
          <input type="radio" class="btn-check" :name="radioGroupName(index)" :id="'btnradio2' + index"
            autocomplete="off" @change="setActiveRadio('Bot', index)"/>
          <label class="btn btn-outline-primary" :for="'btnradio2' + index">Bot</label>
        </div>
        <div v-if="local">
          <input :id="'name' + index" type="text" class="form-control" :value="getPlayerValue(index)" 
          @input="updatePlayerName(index, $event)">
        </div>
        <div v-else>
          <UserSearchDropdown :index="index" @user-selected="handleUserSelected"/>
        </div>
      </div>
    </div>

    <button type="submit" @click="startTournament($event)" class="btn btn-primary">Start Tournament</button>
  </form>
</template>


<script>
import BracketsTournament from './BracketsTournament.vue';

export default {
  components: { BracketsTournament },
  name: 'FormTournament',
  props: ['local', 'loggedInUser'],
  mounted() {
    this.all_players = [];
    this.all_matches = [];
    this.tournamentName = "Quack";
    this.updatePlayerCount();
  },
  data() {
    return {
      all_players: [],
      all_matches: [],
      tournamentSize: [4, 8, 16, 32],
      selectPos: 0,
      nbr_players: '4',
      tournamentStarted: false,
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
    setTournamentName(event) {
      this.tournamentName = event.target.value;
    },
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

    handleUserSelected(userName, index) {
      this.all_players[index - 1].name = userName;
    },

    // Pushes new Player Object into all_players list if the range/number 
    // of players is adjusted 
    updatePlayerCount () {
      const currentCount = this.all_players.length;
      const list_player = ["phipno", "dummy1", "pnolte", "dummy2"]

      if (this.nbr_players > currentCount) {
        for (let i = currentCount + 1; i <= this.nbr_players; i++) {
          this.all_players.push({
            name: list_player[i - 1],
            player_or_bot: 'Player',
            index: i - 1,
          });
        }
      } else if (this.nbr_players < currentCount) {
        // removes players from the all_pllayer list
        this.all_players.splice(this.nbr_players);
      }
    },

    // createMatches() {
    //   this.all_matches = [];
    //   const total_games = this.nbr_players - 1; 
    //   for (let match = 0; match < total_games; match++) {
    //       console.log(Math.log2(total_games) - Math.floor(Math.log2(match + 1)))
    //       this.all_matches.push({
    //         is_round: Math.floor(Math.log2(total_games + 1)) - Math.floor(Math.log2(total_games - match)),
    //         game_nbr: match + 1, 
    //         l_player: -1,
    //         r_player: -1,
    //         l_score: 0,
    //         r_score: 0,
    //       });
    //       if (this.all_matches[match].is_round == 1) {
    //         this.all_matches[match].l_player = this.all_players[match * 2];
    //         this.all_matches[match].r_player = this.all_players[match * 2 + 1];
    //       }
    //     }
    // },

    async startTournament(event) {
      event.preventDefault();
      if (this.tournamentName == "") {
        console.log("Error Tournament Name isnt allowed to be empty")
        return
      }
      // this.createMatches()
      // TODO: needs to call backend for tournament handling which is not yet implementet
      console.log(this.all_players);
      console.log("Tournament handling not yet implemented in backend");
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      try {
        const response = await fetch('/endpoint/tournament/logic/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({'name': this.tournamentName, 'player': this.all_players, }),
        });
        
        const responseData = await response.json()
        console.log('Backend Response:', responseData.data)
        this.all_matches = responseData.data.games
        this.tournamentName = responseData.data.tour_name
        console.log("TourName: ", this.tournamentName)
        console.log("All Matches:", this.all_matches)
        this.tournamentStarted = true;

      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
  },  
};
</script>