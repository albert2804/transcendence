<template>
  <div class="container justify-content-center" style="width:100%">
    <div class="row" style="width: 100%;">
      <h2>Ongoing Tournaments</h2>
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
    </div>
    
    <h2>Ended Tournaments</h2>
    <div class="nes-container is-rounded" style="height:1000%">
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
  </div>
</template>
  
<script>
import TournamentBoxes from './TournamentBoxes.vue';

export default {
  components: { TournamentBoxes },
  name: 'ListTournament',
  props: ['loggedInUser'],
  data() {
      return {
          openTournamentView: 0,
          tournaments: [],
          ongoingTournaments: [],
          endedTournaments: [],
      };
  },
  methods: {
    
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
    top: -3px;
  }

</style>