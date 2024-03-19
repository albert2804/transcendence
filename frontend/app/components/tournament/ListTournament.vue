<template>
  <div class="container justify-content-center" style="width:100%;">
    <div class="row" style="width: 100%;">
      <h3 style="margin-top: 3vh;">Quick Tournament Games</h3>
      <div class="nes-container is-rounded carousel-container">
        <div v-if="quickSelect.length == 0">
          <strong>There is no playable tournament Game for you</strong> 
        </div>
        <div v-else class="carousel slide" id="gameCarousel" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div v-for="(match, index) in quickSelect" :key="match.is_match" class="carousel-item" :class="{ 'active': index === 0 }">
              <GameBox :match="match" :loggedInUser="loggedInUser"></GameBox>
            </div>
          </div>
          <div class="carousel-controls">
            <button style="color: black" class="carousel-control-prev" type="button" data-bs-target="#gameCarousel" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="">Previous</span>
            </button>
            <button style="color: black" class="carousel-control-next" type="button" data-bs-target="#gameCarousel" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="">Next</span>
            </button>
          </div>
        </div>
      </div>
      
      <h3 style="margin-top: 1.5vh;">Ongoing Tournaments</h3>
      <div class="nes-container is-rounded" style="height:100%">
        <button @click="getTournamets(false)" style="width: 100%; height: 100%; background-color: transparent; border-color: transparent;">
          <progress class="nes-progress is-pattern" value="100" max="100"></progress>
        </button>
        <!-- insert here -->
        <div v-if="openTournamentView == 1">
          <div v-if="ongoingTournaments.length == 0">
            <div class="nes-container is-rounded">
              <strong>There is no ongoing tournament</strong>
            </div>
          </div>
          <div v-else>
            <TournamentBoxes ref="TourBoxes" :loggedInUser="loggedInUser" :tournaments="ongoingTournaments" :openTournamentView="openTournamentView"/>
          </div>
        </div>
      </div>

      <h3 style="margin-top: 1.5vh;">Ended Tournaments</h3>
      <div class="nes-container is-rounded" style="height:100%">
        <button @click="getTournamets(true)" style="width: 100%; height: 100%; background-color: transparent; border-color: transparent;">
          <progress class="nes-progress is-pattern" value="100" max="100"></progress>
        </button>
        <!-- insert here -->
        <div v-if="openTournamentView == 2">
          <div v-if="endedTournaments.length == 0">
            <div class="nes-container is-rounded">
              <strong>There is no ended tournament</strong>
            </div>
          </div>
          <div v-else>
            <TournamentBoxes ref="TourBoxes" :loggedInUser="loggedInUser" :tournaments="endedTournaments" :openTournamentView="openTournamentView"/>
          </div>
        </div>
    </div>
      <ErrorMessages :openPopup="PopupMessage" @close-popup="PopupMessage=false" :error="contentError" :message="contentMessage"/>
    </div>
  </div>
  </template>
  
<script>
import TournamentBoxes from './TournamentBoxes.vue';
import GameBox from './GameBox.vue';
import ErrorMessages from '../popup/ErrorMessages.vue';

export default {
  components: {
    TournamentBoxes,
    GameBox,
    ErrorMessages,
  },
  name: 'ListTournament',
  props: ['loggedInUser'],
  data() {
      return {
          openTournamentView: 0,
          tournaments: [],
          ongoingTournaments: [],
          endedTournaments: [],
          quickSelect: [],
          PopupMessage: false,
          contentError: null,
          contentMessage: null,
      };
  },
  mounted() {
    this.getQuickSelectGames();
    this.startPolling()
  },
  beforeUnmount() {
    this.stopPolling();
  },
  beforeUnmount() {
    this.stopPolling();
  },
  methods: {
    startPolling() {
      this.pollingTimer = setInterval(() => {
        this.getQuickSelectGames();
      }, 10000); // Poll every 5 seconds (adjust as needed)
    },
    stopPolling() {
      clearInterval(this.pollingTimer);
    },
    async getQuickSelectGames() {
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
      try {
        const response = await fetch('/endpoint/tournament/getPlayableGames/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });
        const responseData = await response.json();
        if (responseData.error) {
          console.log('Error from Backend:' ,responseData.error);
          this.contentError = responseData.error;
          this.openPopupMessage();
        }
        if (responseData.message) {
          this.contentMessage = responseData.message;
          this.openPopupMessage();
        }
        this.quickSelect = JSON.parse(responseData.data);
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
    async getTournamets(ongoingOrEnded) {
      if (this.openTournamentView == 0) {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
        try {
          const response = await fetch('/endpoint/tournament/getTournaments/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ name: this.loggedInUser, ongoingOrEnded: ongoingOrEnded}),
          });
          const responseData = await response.json();
          if (responseData.error) {
            console.log('Error from Backend:' ,responseData.error);
            this.contentError = responseData.error;
            this.openPopupMessage();
          }
          if (responseData.message) {
            this.contentMessage = responseData.message;
            this.openPopupMessage();
          }
          this.tournaments = JSON.parse(responseData.data);
          this.tournaments.forEach((tournament) => {
            tournament.showTournament = false;
            if (ongoingOrEnded)
              this.endedTournaments.push(tournament);
            else
              this.ongoingTournaments.push(tournament);
            });
          if (ongoingOrEnded)
            this.openTournamentView = 2;
          else
            this.openTournamentView = 1;
        } catch (error) {
          console.log('Error sending signal to backend:', error);
        }
      }
      else {
        if (this.ongoingTournaments.length != 0)
          this.$refs.TourBoxes.stopPollingOfAll();
        this.openTournamentView = 0;
        this.tournaments = [];
        this.ongoingTournaments = [];
        this.endedTournaments = [];
      }
    },
    openPopupMessage() {
      this.PopupMessage = true
      console.log('Value of PopupMessage: ', this.PopupMessage);
    },
  },
};
</script>

<style>
  .nes-progress{
    position: relative;
    top: 0;
    transition: linear 0.1s;
  }
  .nes-progress:hover{
    top: 3px;
  }

  h3 {
    padding-top: 2%;
  }
  .carousel-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }

  .carousel-controls {
    display: flex;
    justify-content: space-between;
  }

  .carousel-control-prev, .carousel-control-next {
  position: absolute;
  bottom: 0;
  transform: translateY(-50%);
}

</style>