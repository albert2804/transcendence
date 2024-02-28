<template>
  <div class="container mt-5">
    <div class="bracket">
      <div v-for="(round, index) in rounds" :key="index" class="round list-group nes-container is-rounded d-flex flex-column">
        <h3>R O U N D  <span>{{ round }}</span></h3>
        <div v-for="match in getMatches(round)" :key="match.is_match" class="match list-group-item nes-container is-rounded position-relative">
        <!-- @mouseover="togglePlayButton(match.is_match, true)" @mouseleave="togglePlayButton(match.is_match, false)"> -->
          <p>{{ match.is_match }}.</p>
          <div>
            <p>{{ match.player1 }}</p>
            <p>{{ match.pointsP1 }}</p>
          </div>
          <div class="user">
            <p>{{ match.player2 }}</p>
            <p>{{ match.pointsP2 }}</p>
          </div>
          <div v-if="(match.player1 == this.loggedInUser || match.player2 == this.loggedInUser) && this.loggedInUser != undefined && match.finished == false"
          class="position-absolute w-100 h-100 d-flex align-items-center justify-content-center">
            <button class="btn" :class="{ goGreen: playerReady }" @click="sendReadyPlayer($event, match.is_match)">
              <span v-if="playerReady">You are Ready</span><span v-else>Play</span></button>
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
      showPlayButtons: [],
      matches: [],
      // No need for additional data in this case
    };
  },
  mounted() {
    this.refreshMatcheshData();
    this.matches.forEach((match) => {
      this.showPlayButtons.push(false);
    });
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
    togglePlayButton(index, bool) {
      this.showPlayButtons[index] = bool;
    },
    startPolling() {
      this.pollingTimer = setInterval(() => {
        this.refreshMatcheshData();
      }, 10000); // Poll every 5 seconds (adjust as needed)
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
.container {
  max-width: 1200px;
  margin: auto;
  padding: 0 20px;
}

.bracket {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.user {
  display: flex;
  flex-direction: column;
}
.round {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background-color: #fff;
  border-radius: 10px;
  margin-bottom: 20px;

}

.match {
  display: flex;
  flex-direction: columns;
  align-items: center;
  width: 100%;
  background-color: #fff;
  margin-bottom: 10px;
}
.btn {  
  position: absolute;
  width: 77%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0;
  background-color: transparent;
  box-shadow: none;
  color: transparent;
}

.btn:hover { 
  background-color: #ff7c7c;
  color: black;
}
.goGreen {
  background-color: #99e857;
  color: black;
}
</style>
