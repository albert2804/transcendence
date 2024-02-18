<template>
  <div class="user-stats">
    <h2>User Statistics</h2>
    <div v-if="userStats.username != ''">
      <p>Username: {{ userStats.username }}</p>
      <p>Alias: {{ userStats.alias }}</p>
      <p>Date Joined: {{ userStats.date_joined }}</p>
      <p>Games Won: {{ userStats.games_won }}</p>
      <p>Games Played: {{ userStats.games_played }}</p>
      <p>Matchmade Ranking: {{ userStats.mmr }}</p>
      <p>Overall Ranking: {{ userStats.ranking }}</p>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  name: 'InfoComponent',
    data() {
     return {
      userStats: {
        username: '',
        games_played: '0',
        games_won: '0',
        alias: '',
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
    }
  }
}
</script>

<style>
  /* .card-size {
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
  } */
</style>