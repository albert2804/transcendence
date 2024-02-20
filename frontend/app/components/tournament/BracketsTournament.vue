<template>
  <div class="container mt-5">
    <div class="bracket">
      <div v-for="(round, index) in rounds" :key="index" class="round list-group">
        <div v-for="match in getMatches(round)" :key="match.id" class="match list-group-item">
          <p>Round {{ match.is_round }}, Match {{ match.game_nbr }}</p>
          <p>Left Player: {{ match.l_player }}</p>
          <p>Right Player: {{ match.r_player }}</p>
          <p>Left Score: {{ match.l_score }}</p>
          <p>Right Score: {{ match.r_score }}</p>
          <div v-if="match.l_player == this.loggedInUser || match.r_player == this.loggedInUser && this.loggedInUser != undefined">
            <button class="nes-btn" @click="sendReadyPlayer($event, match.game_nbr)">Play</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'BracketsTournament',
  props: ['numberOfPlayers', 'matches', 'loggedInUser', 'tournamentName'],
  data() {
    return {
      playerReady: false,
      // No need for additional data in this case
    };
  },
  computed: {
    rounds() {
      return Math.log2(this.numberOfPlayers);
    },
  },
  methods: {
    async sendReadyPlayer(event, game_index) {
      event.preventDefault();
      this.playerReady = !this.playerReady;
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      try {
        const response = await fetch('/endpoint/tournament/readyPlayer/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({username: this.loggedInUser, isPlayerReady:this.playerReady, game_index: game_index, tour_name: this.tournamentName}),
        });

        const responseData = await response.json();
        console.log('Backend response:', responseData);
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
    getMatches(round) {
      console.log(this.loggedInUser)
      return this.matches.filter(match => match.is_round === round);
    },
  },
};
</script>

<style scoped>
.bracket {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.round {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.match {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>
