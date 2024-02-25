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
  <div class="game-history">
    <h2>Game History</h2>
    <div v-if="game_history.length  && isLoggedIn === 1">
      <table>
        <thead>
          <tr>
            <th>Game ID</th>
            <th>Player 1</th>
            <th>Player 2</th>
            <th>Game Length</th>
            <th>Winner</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(game, index) in game_history" :key="index">
            <td>{{ game.id }}</td>
            <td>{{ game.player1 }}</td>
            <td>{{ game.player2 }}</td>
            <td>{{ game.time }}</td>
            <td>{{ game.winner }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else>No game history available</p>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  name: 'GameHistory',
    data() {
     return {
      game_history: [],
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
        this.data = await response.json();
        this.game_history = this.data.game_history
      } catch (error) {
        console.error('Error:', error)
      }
    },
  }
}
</script>

<style>
  .game-history {
    width: 100%;
    margin-top: 20px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  th, td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
  }

  tbody tr:nth-child(even) {
    background-color: #f2f2f2;
  }
</style>