<template>
  <div class="container is-centered">
    <div class="row" style="width: 100%;">
      <h2>Ongoing Tournaments</h2>
      <div class="nes-container is-rounded" style="height:100%">
        <button @click="getTournamets" style="width: 100%; height: 100%; background-color: transparent; border-color: transparent;">
          <progress class="nes-progress is-pattern" value="100" max="100"></progress>
        </button>
        <!-- insert here -->
        <div v-if="openOngoing">
          <div v-if="ongoingTournaments.length == 0">
            <div class="nes-container is-rounded">
              <strong>There is no ongoing tournament</strong>
            </div>
          </div>
          <div v-else>
            <div v-for="(tournament, index) in ongoingTournaments" :key="index"
              class="nes-container is-rounded">
              <div>
                <strong>Tournament Name:</strong> {{ tournament.tournament_name }}<br>
                <strong>Created At:</strong> {{ tournament.created_at }}
                <button :id="'tournament' + index" @click="showTournamentDetails(index)" style="width: 100%; height: 100%; background-color: transparent; border-color: transparent;">
                  <progress style="height: 15px;" class="nes-progress is-pattern" value="100" max="100"></progress>
                </button>
              </div>
              <div v-if="ongoingTournaments[index].showTournament">
                <BracketsTournament :loggedInUser="loggedInUser" :matches="tournament.games" :tournamentName="tournament.tournament_name"/>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <h2>Ended Tournaments</h2>
      <div class="nes-container is-rounded">

      </div>
    </div>
  </div>
</template>
  
<script>
import BracketsTournament from './BracketsTournament.vue';

export default {
    name: 'ListTournament',
    props: ['loggedInUser'],
    data() {
        return {
            openOngoing: false,
            tournaments: [],
            ongoingTournaments: [],
        };
    },
    methods: {
      showTournamentDetails(index) {
        console.log(this.ongoingTournaments[index].showTournament + index)
        this.ongoingTournaments[index].showTournament = !this.ongoingTournaments[index].showTournament;
      },

      async getTournamets() {
          if (!this.openOngoing) {
              const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
              try {
                  const response = await fetch('/endpoint/tournament/getTournaments/', {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json',
                          'X-CSRFToken': csrfToken,
                      },
                      body: JSON.stringify({ name: this.loggedInUser }),
                  });
                  const responseData = await response.json();
                  this.tournaments = JSON.parse(responseData.data);
                  console.log('Backend response:', responseData);
                  this.tournaments.forEach((tournament) => {
                    tournament.showTournament = false;
                    this.ongoingTournaments.push(tournament);
                  });
                  this.openOngoing = true;
              }
              catch (error) {
                  console.log('Error sending signal to backend:', error);
              }
          }
          else {
              this.openOngoing = false;
              this.tournaments = [];
              this.ongoingTournaments = [];
          }
      },
    },
    components: { BracketsTournament }
};
</script>

<style>
  .nes-progress{
    position: relative;
    top: 0;
    transition: linear 0.1s;
  }
  .nes-progress:hover{
    top: -3px
  }

</style>