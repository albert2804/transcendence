<template>
  <div class="container" v-if="fetched">
    <h1 class="text-center">Leaderboard</h1>
      <table class="nes-table is-bordered table-hover">
        <thead class="thread-dark">
          <tr>
            <th scope = "col">#</th>
            <th scope="col">Username</th>
            <th scope="col">Games<br> Won</th>
            <th scope="col">MMR</th>
            <th scope="col">Games<br> Played</th>
            <th scope="col">Win<br> Ratio</th>
            <th v-if="loginStatus" scope="col">User <br> profile</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in sortedUsers" :key="user.mmr">
            <th scope = "row">{{ index + 1}}</th>
            <td>{{ user.username }}</td>
            <td>{{ user.num_games_won }}</td>
            <td>{{ user.mmr }}</td>
            <td>{{ user.num_games_played }}</td>
            <td>{{ (user.num_games_played !== 0) ? (( user.num_games_won / user.num_games_played) * 100).toFixed(0) + '%' : '0%' }}</td>
            <td v-if="loginStatus">
              <router-link :to="{ name: 'userinfopage', query: { username: user.username } }">
                <button type="button" class="btn nes-btn btn-primary profile-button"><span>View Profile</span></button>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
  </div>
</template>

<script>
import { isLoggedIn } from '~/store';
export default {
	data()
  {
    return { 
      users: [],
      fetched: false,
      loginStatus: false
    };
  },
	mounted() 
  {
    this.fetchUsers();

    watchEffect(() => {
      if (isLoggedIn.value === 1) {
        this.loginStatus = true;
      } else {
        this.loginStatus = false;
      }
    });
  },
  computed: 
  {
    sortedUsers() 
    {
      return this.users.slice().sort((a, b) => b.mmr - a.mmr);
    }
  },
  methods: 
  {
    async fetchUsers() 
    {
      try 
      {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        let url = '/endpoint/user/get_all_users?attributes=username,alias,num_games_played,num_games_won,mmr';
        const response = await fetch(url, {
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
        this.fetched = true;
      } 
      catch (error) 
      {
        console.error('Error:', error)
      }
    }
  }
}
</script>

<style>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.nes-table.is-bordered{
  max-width: 100%;
  font-size: 1.0em;
}

.nes-table.is-bordered * {
  font-size: inherit;
}

@media screen and (max-width: 1200px) {
  .nes-table.is-bordered {
	font-size: 0.8em; 
  }
}

@media screen and (max-width: 800px) {
  .nes-table.is-bordered {
	font-size: 0.7em; 
  }
}

@media screen and (max-width: 575px) {
  .nes-table.is-bordered {
	font-size: 0.5em;
  }
}

.profile-button {
  max-width: 100%;
}
</style>