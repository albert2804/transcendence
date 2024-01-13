<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
  <div class="user-stats">
    <h2>User Statistics</h2>
    <div v-if="userStats.username != ''">
      <p>Username: {{ userStats.username }}</p>
      <p>Date Joined: {{ userStats.date_joined }}</p>
      <p>Games Played: {{ userStats.games_played }}</p>
      <p>Matchmade Ranking: {{ userStats.mmr }}</p>
      <p>Overall Ranking: {{ userStats.ranking }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfoComponent',
    data() {
    return {
      userStats: {
        username: '',
        date_joined: '',
        games_played: '0',
        mmr: '0',
        ranking: '0',
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
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/user/info', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          }
        })
        this.userStats = await response.json();
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }
}
</script>

<style>
  .card-size {
    min-width: px;
    max-width: 400px;
  }
  .button-list {
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .shade-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(255,255,255,0.7);
  }
</style>