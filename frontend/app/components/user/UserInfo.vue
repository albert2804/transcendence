<script setup>
import { isLoggedIn, userName, userId } from '~/store';
watchEffect(() => {
  if (!isLoggedIn.value) {
    isLoggedIn.value = isLoggedIn.value;
    userName.value = userName.value;
    userId.value = userId.value;
  }
});
</script>

<template>
  <div class="user-stats">
    <h2>User Statistics</h2>
    <div v-if="userStats.username != ''">
      <p>Username: {{ userStats.username }}</p>
      <p>Alias: {{ userStats.alias }}</p>
      <p>Date Joined: {{ userStats.date_joined }}</p>
      <p>Games Won: {{ userStats.games_won }}</p>
      <p>Games Lost: {{ userStats.games_lost }}</p>
      <p>Games Played: {{ userStats.games_played }}</p>
      <p>Matchmade Ranking: {{ userStats.mmr }}</p>
      <button v-if="userStats.username != userName && isLoggedIn" type="button" class="btn nes-btn btn-primary block-button" @click="inviteToGame">Invite to Game</button>
      <button v-if="userStats.username != userName && isLoggedIn && !userStats.friend" type="button" class="btn nes-btn btn-primary block-button" @click="addFriend">Add Friend</button>
	  <button v-if="userStats.username != userName && isLoggedIn && userStats.friend" type="button" class="btn nes-btn btn-primary block-button" @click="removeFriend">Remove Friend</button>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  name: 'UserInfo',
    data() {
     return {
      userStats: {
        username: '',
        games_played: '0',
        games_won: '0',
        games_lost: '0',
        alias: '',
        ranking: '0',
		friend: false,
      },
      error: '',
    };
  },

  mounted() {
    this.fetchStatistics();
  },
  methods: {
    async fetchStatistics() {
      try {
        const route = useRoute();
        const username = route.query.username;
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const params = new URLSearchParams({ username: username });
        const response = await fetch(`/endpoint/user/info?${params.toString()}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          }
        });
        this.userStats = await response.json();
      } catch (error) {
        console.error('Error:', error)
      }
    },
    async inviteToGame() {
      try {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/api/invite_to_game', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            'receiver': this.userStats.username
          })
        });
      }
      catch (error) {
        console.error('Error:', error)
      }
    },
    async addFriend() {
      try {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/api/add_friend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            'receiver': this.userStats.username
          })
        });
      }
      catch (error) {
        console.error('Error:', error)
      }
    },
	async removeFriend() {
	  try {
		const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
		const response = await fetch('/endpoint/api/remove_friend', {
		  method: 'POST',
		  headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken
		  },
		  body: JSON.stringify({
			'receiver': this.userStats.username
		  })
		});
	  }
	  catch (error) {
		console.error('Error:', error)
	  }
	}
  }
}
</script>

<style>
  .block-button {
    display: block;
    /* width: 100%; */
    margin-top: 10px;
  }
</style>