<template>
  <div v-if="loginStatus === 1">
    <div>
      <h1>Youre on the tournament site</h1>
      <button v-if="isDevelopment" @click="callSignUp" class="btn btn-primary"></button>
      <div>
        <button @click="toggleForm" class="btn btn-primary">
        {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
      </div>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false" :loggedInUser="loggedInUser"/>
    </div>
    <div>
      <ListTournament :loggedInUser="loggedInUser"/>
    </div>
  </div>
  <div v-else-if="loginStatus === 0" class="center-screen">
    <div>
      <div class="nes-container is-rounded" style="width: 50%; margin: 0 auto;">
        <h3>Only members can see this page</h3>
      </div>
    </div>
  </div>
</template>

<script>
import FormTournament from '~/components/tournament/FormTournament.vue';
import ListTournament from '~/components/tournament/ListTournament.vue';
import { isLoggedIn, userName } from '~/store';

export default {
  components: {FormTournament, ListTournament}, 
  data() {
    return {
      formVisible: false,
      loginStatus: isLoggedIn,
      loggedInUser: userName,
      isDevelopment: process.env.NODE_ENV === 'development'
    };
  },
  watch: {
    isLoggedIn: {
      handler(newValue) {
        this.loginStatus = newValue;
        console.log("loginStatus: " + this.loginStatus);
      }
    },
    userName: {
      handler(newValue) {
        this.loggedInUser = newValue;
        console.log("loggedInUser: " + this.loggedInUser);
      }
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

<style>
.center-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 75vh;
}
</style>