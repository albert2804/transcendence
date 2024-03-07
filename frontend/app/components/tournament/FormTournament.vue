<template>
  <div class="nes-container is-rounded">
    <form style="max-width: 1000px; margin: auto; overflow: hidden;">
      <div class="nes-field">
        <label for="name_field" class="float-start" style="margin-top: 3vh;">Tournament Name</label>
        <input type="text" id="name_field" class="nes-input" placeholder="Your Tournament Name" @input="setTournamentName($event)">
      </div>
      <div class="mb-3" style="margin-top: 4vh;">
        <label for="nbrPlayerRange" class="form-label float-start" style="margin-right: 50px;">Total Players: </label>
        <div class="d-flex align-items-center">
          <input style="width: 80%; " type="range" class="form-range" min="0" max="3" step="1" id="nbrPlayerRange" 
            v-model.number="selectPos" @input="updatePlayerCount">
          <h6 style="rotate:90deg;" class="ms-3">{{ selectedData }}</h6>
        </div>
      </div>

      <div style="margin-bottom: 3%;" class="name-box row flex-wrap">
        <div v-for="index in nbr_players" style="min-width: 50%; margin-bottom: 1%" :key="index" class="name-input d-flex col-12 col-lg-1">
          <!-- this is for bots -->
          <!--<div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input type="radio" class="btn-check" :name="radioGroupName(index)" :id="'btnradio1' + index"
              autocomplete="off" checked @change="setActiveRadio('Player', index)"/>
            <label class="btn btn-outline-primary" :for="'btnradio1' + index">Player</label>
            <input type="radio" class="btn-check" :name="radioGroupName(index)" :id="'btnradio2' + index"
              autocomplete="off" @change="setActiveRadio('Bot', index)"/>
            <label class="btn btn-outline-primary" :for="'btnradio2' + index">Bot</label>
          </div> -->
          <p style="font-size: 1rem;" class="nes-text is-primary" :for="'btnradio1' + index">P {{ index }}:</p>
          <div v-if="local">
            <input :id="'name' + index" type="text" class="form-control" :value="getPlayerValue(index)" 
            @input="updatePlayerName(index, $event)">
          </div>
          <div v-else>
            <UserSearchDropdown :index="index" @user-selected="handleUserSelected"/>
          </div>
        </div>
        <ErrorMessages :openPopup="PopupMessage" @close-popup="PopupMessage=false" :error="contentError" :message="contentMessage"/>
    </div>

      <button type="submit" @click="startTournament($event)" class="nes-btn is-primary" style="margin-bottom: 3vh;">Start Tournament</button>
    </form>
  </div>
</template>


<script>
import BracketsTournament from './BracketsTournament.vue';
import ErrorMessages from '../popup/ErrorMessages.vue';

export default {
  components: {
    BracketsTournament,
    ErrorMessages,
  },
  name: 'FormTournament',
  props: ['local', 'loggedInUser'],
  mounted() {
    this.all_players = [];
    this.all_matches = [];
    this.tournamentName = '';
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
      PopupMessage: false,
      contentError: null,
      contentMessage: null,
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

    async updatePlayerName(index, event) {
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
      // const list_player = ["phipno", "dummy1", "pnolte", "dummy2"]

      if (this.nbr_players > currentCount) {
        for (let i = currentCount + 1; i <= this.nbr_players; i++) {
          this.all_players.push({
            name: "",
            player_or_bot: 'Player',
            index: i - 1,
          });
        }
      } else if (this.nbr_players < currentCount) {
        // removes players from the all_pllayer list
        this.all_players.splice(this.nbr_players);
      }
    },

    refreshNames () {
      this.all_players.forEach((player) => {
        player.name = '';
      });
    },

    async startTournament(event) {
      event.preventDefault();
      if (this.tournamentName == "") {
        this.contentError = "Error: Tournament Name isn't allowed to be empty";
        this.contentMessage = '';
        this.openPopupMessage();
        return
      }
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
        if (responseData.error) {
          this.contentError = responseData.error;
          this.contentMessage = '';
          this.openPopupMessage();
          return
        }
        else if (responseData.message) {
          this.contentMessage = responseData.message;
          this.openPopupMessage();
        }
        this.all_matches = responseData.data.games
        this.tournamentName = responseData.data.tour_name
        this.tournamentStarted = true;
        this.contentMessage = "Successfully created tournament";
        this.openPopupMessage();
        this.refreshNames();
        // this.contentMessage = "";
      } catch (error) {
          console.log('Error sending signal to backend', error);
      }
    },
    openPopupMessage() {
      this.PopupMessage = true
        // console.log('Value of PopupMessage: ', this.PopupMessage);
    },
  },  
};
</script>