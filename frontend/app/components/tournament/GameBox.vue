<template>
  <div class="gamebox">
    <div>
      <h5>Tournament {{ match.tournament_name }}</h5>
      <p>Match {{ match.is_match }}.</p>
    </div>
    <div style="height: 100%; width: 100%;" >
      <div class="users">
        <div class="user">
          <p>{{ match.player1 }}</p>
          <p>Score: {{ match.pointsP1 }}</p>
        </div>
        
        <div v-if="(match.player1 == this.loggedInUser || match.player2 == this.loggedInUser) && this.loggedInUser != undefined && match.finished == false" class="play-button-container">
          <button class="nes-btn nes-btn-gamebox is-success" @click="sendInvite($event)"> 
            <span>Play</span>
          </button>
        </div>
        <div class="user">
          <p>{{ match.player2 }}</p>
          <p>Score: {{ match.pointsP2 }}</p>
        </div>
      </div>
    </div>
     <ErrorMessages :openPopup="PopupMessage" @close-popup="PopupMessage=false" :error="contentError" :message="contentMessage"/>
  </div>
</template>

<script>
import ErrorMessages from '../popup/ErrorMessages.vue';
export default {
  components: {
    ErrorMessages,
  },
  name: 'GameBox',
  props: ['match', "loggedInUser", "tournament_name"],
  data() {
    return {
      PopupMessage: false,
      contentError: null,
      contentMessage: null,      
    };
  },
  methods: {
    async sendInvite(event) {
      event.preventDefault();
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      let tour_name;
      if (this.match.tournament_name)
        tour_name = this.match.tournament_name;
      else
        tour_name = this.tournament_name;
      try {
        const response = await fetch('/endpoint/tournament/inviteOtherPlayer/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({username: this.loggedInUser, game_nbr: this.match.is_match, tour_name: tour_name}),
        });
        if (responseData.error) {
          console.log('Error from Backend:' ,responseData.error);
          this.contentError = responseData.error;
          this.openPopupMessage();
        }
        if (responseData.message) {
          console.log('Message from Backend: ', responseData.message);
          this.contentMessage = responseData.message;
          this.openPopupMessage();
        }
        const responseData = await response.json();
      } catch (error) {
        // console.log('Error sending signal to backend:', error);
      }
    },
    openPopupMessage() {
      this.PopupMessage = true
      console.log('Value of PopupMessage: ', this.PopupMessage);
    },
  }
}

</script>

<style>
.gamebox {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.users {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
}

.user {
  flex: 1 0 auto;
  border: 5px #ff7c7c;
  border-style: dashed solid;
  padding: 10px;
  margin-bottom: 10px;
  margin: 10px;
}

.users {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch; /* New property */
  width: 100%;
  margin: auto;
}

.user p {
  margin: 0;
  padding: 0;
}

.play-button-container {
  display: flex;
  align-items: center; /* New property */
}

.nes-btn-gamebox {
  height: 50%;
  margin: auto;
}
</style>