<template>
  <div>
    <p>Match {{ match.is_match }}.</p>
    <div class="user">
      <p>{{ match.player1 }}</p>
      <p>Score: {{ match.pointsP1 }}</p>
    </div>
    <div class="user">
      <p>{{ match.player2 }}</p>
      <p>Score: {{ match.pointsP2 }}</p>
    </div>
    <div v-if="(match.player1 == this.loggedInUser || match.player2 == this.loggedInUser) && this.loggedInUser != undefined && match.finished == false">
      <button class="nes-btn" @click="sendInvite($event)">
        <span>Play</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameBox',
  props: ['match', "loggedInUser", "tournament_name"],
  methods: {
    async sendInvite(event) {
      event.preventDefault();
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      let tour_name;
      console.log(this.match.tournament_name)
      console.log(this.tournament_name)
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

        const responseData = await response.json();
        console.log('Backend response:', responseData);
      } catch (error) {
        console.log('Error sending signal to backend:', error);
      }
    },
  }
}

</script>

<style>
.user {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.user p {
  margin: 0;
  padding: 0;
}
</style>