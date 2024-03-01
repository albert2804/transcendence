<template>
  <div>
    <div v-for="(tournament, index) in tournaments" :key="index"
    class="nes-container is-rounded" style="width: 100%">
    <div>
      <strong>Tournament Name:</strong> {{ tournament.tournament_name }}<br>
      <strong>Created At:</strong> {{ tournament.created_at }}
      <button :id="'tournament' + index" @click="showTournamentDetails(index)" style="width: 100%; height: 100%; background-color: transparent; border-color: transparent;">
        <progress style="height: 15px;" class="nes-progress is-pattern" value="100" max="100"></progress>
      </button>
    </div>
    <div v-if="tournaments[index].showTournament">
      <h2>{{tournament.tournament_name}}</h2>
      <BracketsTournament :ref="`BracketsTournament-${index}`" :loggedInUser="loggedInUser" :tournamentName="tournament.tournament_name"/>
    </div>
  </div>
</div>
</template>

<script>
import BracketsTournament from './BracketsTournament.vue';

export default {
  components: { BracketsTournament },
  name: 'TournamentBoxes',
  props: ['tournaments', 'loggedInUser', 'openTournamentView'],
  methods: {
    stopPollingOfAll() {
      if (this.openTournamentView == 1){
        this.tournaments.forEach((tournament, i) => {
          if (tournament.showTournament == true) {
            this.$nextTick(() => {
              this.$refs[`BracketsTournament-${i}`][0].stopPolling();
            });
          }
        });
      }
    },
    showTournamentDetails(index) {
      console.log("INDEX IS " + this.tournaments[index].showTournament + index)
      if (this.tournaments[index].showTournament) {
        if (this.openTournamentView == 1){
          this.$nextTick(() => {
            this.$refs[`BracketsTournament-${index}`][0].stopPolling();
            this.tournaments[index].showTournament = false;
          });
        }
        else
          this.tournaments[index].showTournament = false;
      }
      else {
        this.tournaments[index].showTournament = true;
        if (this.openTournamentView == 1){
          this.$nextTick(() => {
            this.$refs[`BracketsTournament-${index}`][0].startPolling();
          });
        }
        this.tournaments.forEach((tournament, i) => {
          console.log(i)
          if (i != index && tournament.showTournament == true) {
            if (this.openTournamentView == 1){
              this.$nextTick(() => {
                this.$refs[`BracketsTournament-${i}`][0].stopPolling();
                tournament.showTournament = false;  
              });
            }
            else
              tournament.showTournament = false;  
          }
        });
      }
    },
  },
};
</script>

<style>

</style>