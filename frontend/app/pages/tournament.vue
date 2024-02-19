<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value;
  })
</script>

<template>
  <div>
    <div>
      <h1>Youre on the tournament site</h1>
      <button @click="callSignUp" class="btn btn-primary"></button>
      <div v-if="isLoggedIn">
        <button @click="toggleForm" class="btn btn-primary">
        {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
      </div>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false" :loggedInUser="loggedInUser"/>
    </div>
    <div v-if="isLoggedIn">
      <ListTournament />
    </div>
  </div>
</template>

<script>
import FormTournament from '~/components/tournament/FormTournament.vue';
import ListTournament from '~/components/tournament/ListTournament.vue'

export default {
  components: {FormTournament, ListTournament}, 
  data() {
    return {
      formVisible: false,
      loggedInUser: "",
    };
  },
  async mounted() {
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
      const data = await response.json();
      console.log(data)
      this.loggedInUser = data.username;
      console.log(this.loggedInUser)
    } catch (error) {
      console.error('Error:', error)
    }
  },
  methods: {
    toggleForm() {
      this.formVisible = !this.formVisible
    },

    //adds two dummy users to the game
    async callSignUp() {
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
      const response = await fetch('/endpoint/tournament/sign_up/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: null,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status ${response.status}`);
      }
    },
  }
}
</script>