<template>
  <div class="container mt-5">
    <div class="bracket">
      <div v-for="(round, index) in rounds" :key="index" class="round list-group">
        <div v-for="match in getMatches(round)" :key="match.is_match" class="match list-group-item">
          <p>Round {{ match.is_round }}, Match {{ match.is_match }}</p>
          <p>Player 1: {{ match.player1 }}</p>
          <p>Player 2: {{ match.player2 }}</p>
          <p>Player1 Score: {{ match.pointsP1 }}</p>
          <p>Player2 Score: {{ match.pointsP2 }}</p>
          <div v-if="(match.player1 == this.loggedInUser || match.player2 == this.loggedInUser) && this.loggedInUser != undefined && match.finished == false">
            <button class="nes-btn" :class="{ goGreen: playerReady }" @click="sendReadyPlayer($event, match.is_match)">Play</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'BracketsTournament',
  props: ['loggedInUser', 'tournamentName'],
  data() {
    return {
      playerReady: false,
      matches: [],
      // No need for additional data in this case
    };
  },
  mounted() {
    this.refreshMatcheshData();
  },
  beforeDestroy() {
    this.stopPolling();
  },
  computed: {
    rounds() {
      //this needs the amount of total players in the tournament
      // console.log(Math.log2(this.matches.length + 1))
      return Math.log2(this.matches.length + 1);
    },
  },
  methods: {
    startPolling() {
      this.pollingTimer = setInterval(() => {
        this.refreshMatcheshData();
      }, 5000); // Poll every 5 seconds (adjust as needed)
    },
    stopPolling() {
      clearInterval(this.pollingTimer);
    },
    async refreshMatcheshData() {
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      try {
        const response = await fetch('/endpoint/tournament/getTourmaentsGames/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({tournamentName: this.tournamentName})
        });

        const responseData = await response.json();
        this.matches = JSON.parse(responseData.data);
        this.matches = this.matches.games
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
    async sendReadyPlayer(event, game_index) {
      event.preventDefault();
      this.playerReady = !this.playerReady;
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      try {
        const response = await fetch('/endpoint/tournament/iviteOtherPlayer/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({username: this.loggedInUser, isPlayerReady:this.playerReady, game_nbr: game_index, tour_name: this.tournamentName}),
        });

        const responseData = await response.json();
        console.log('Backend response:', responseData);
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
    getMatches(round) {
      // console.log(round)
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

.goGreen {
  background-color: greenyellow;
}
</style>
