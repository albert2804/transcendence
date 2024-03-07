<template>
  <div class="container mt-5">
    <div class="bracket">
      <div v-for="(round, index) in rounds" :key="index" class="round list-group nes-container is-rounded d-flex flex-column">
        <h3>R O U N D  <span>{{ round }}</span></h3>
        <div v-for="match in getMatches(round)" :key="match.is_match" class="match list-group-item nes-container is-rounded position-relative">
        <!-- @mouseover="togglePlayButton(match.is_match, true)" @mouseleave="togglePlayButton(match.is_match, false)"> -->
          <GameBox :match="match" :loggedInUser="loggedInUser" :tournament_name="tournamentName"></GameBox>
        </div>
         <ErrorMessages :openPopup="PopupMessage" @close-popup="PopupMessage = false" :error="contentError" :message="contentMessage"/>
      </div>
    </div>
  </div>
</template>

<script>
import GameBox from './GameBox.vue';
import ErrorMessages from '../popup/ErrorMessages.vue';

export default {
  components: {
    GameBox,
    ErrorMessages,
  },
  name: 'BracketsTournament',
  props: ['loggedInUser', 'tournamentName'],
  data() {
    return {
      playerReady: false,
      showPlayButtons: [],
      matches: [],
      PopupMessage: false,
      contentError: null,
      contentMessage: null,
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
        if (responseData.error) {
          console.log('Error from Backend:', responseData.error);
          this.contentError = responseData.error;
          this.openPopupMessage();
        }
        if (responseData.message) {
          this.contentMessage = responseData.message;
          this.openPopupMessage();
        }
        this.matches = JSON.parse(responseData.data);
        this.matches = this.matches.games
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
    getMatches(round) {
      // console.log(round)
      return this.matches.filter(match => match.is_round === round);
    },
    openPopupMessage() {
      this.PopupMessage = true
      // contentMessage = ('message-from-component', label, content);
    },
  },
};
</script>
