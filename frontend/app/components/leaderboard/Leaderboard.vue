<template>
  <div class="container-fluid vh-100">
      <h1 class="text-center">Leaderboard</h1>
      <table class="table table-striped table-hover">
        <thead class="thread-dark">
          <tr>
            <th scope = "col">#</th>
            <th scope="col">Username</th>
            <th scope="col">Games Won</th>
            <th scope="col">Games Played</th>
            <th scope="col">Win Ratio</th>
            <th scope="col">User profile</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in sortedUsers" :key="user.username">
            <th scope = "row">{{ index + 1}}</th>
            <td>{{ user.username }}</td>
            <td>{{ user.num_games_won }}</td>
            <td>{{ user.num_games_played }}</td>
            <td>{{ user.num_games_played / user.num_games_won }}</td>
            <td>
              <router-link :to="{ name: 'userinfopage', query: { username: user.username } }">
                <button type="button" class="btn btn-primary">View Profile</button>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
  </div>
</template>

<script>
export default {
	data()
  {
    return { users: []	};
  },
	created() 
  {
    this.fetchUsers();
	},
  computed: 
  {
    sortedUsers() 
    {
      return this.users.slice().sort((a, b) => b.num_games_won - a.num_games_won);
    }
  },
  methods: 
  {
    async fetchUsers() 
    {
      try 
      {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/user/get_all_users?attributes=username,alias,num_games_played,num_games_won', 
          {
            method: 'GET',
            headers: 
            {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            }
          }
        )
        const jsonResponse = await response.json();
        this.users = jsonResponse.response;
      } 
      catch (error) 
      {
        console.error('Error:', error)
      }
    }
  }
}
</script>

<style scoped>
.vh-100 {
  height: 100vh; /* Set the height to 100% of the viewport height */
}
</style>