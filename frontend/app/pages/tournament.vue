<template>
  <div v-if="loginStatus === 1">
    <div class="container justify-content-center">
      <h1>Youre on the tournament site!</h1> 
    </div>
    <ListTournament :loggedInUser="loggedInUser"/>
    <div style="align-items: center; margin-top: 4vh;">
      <p style=""><strong>For Evaluation: </strong>
        <button v-if="isDevelopment" @click="callSignUp" class=" nes-btn nes-btn-tour is-error">Create 3 Dummy Accounts</button>
      </p>
      <button @click="toggleForm" class="nes-btn is-primary row" style="min-width: 300px; margin-top: 3vh;">
          {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false" :loggedInUser="loggedInUser"/>
    </div>
    <ErrorMessages :openPopup="PopupMessage" @close-popup="PopupMessage=false" :error="contentError" :message="contentMessage"/>
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
import { isLoggedIn, userName } from '~/store';;
import ErrorMessages from '../components/popup/ErrorMessages.vue';

export default {
  components: {FormTournament, ListTournament, ErrorMessages}, 
  data() {
    return {
      formVisible: false,
      loginStatus: isLoggedIn,
      loggedInUser: userName,
      isDevelopment: process.env.NODE_ENV === 'development',
      PopupMessage: false,
      contentError: null,
      contentMessage: null,
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
    },
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
      this.loggedInUser = data.username;
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
      const responseData = await response.json()
      if (responseData.error) {
        console.log('Error from Backend:' ,responseData.error);          
        this.contentError = responseData.error;
        this.openPopupMessage();
      }
      if (responseData.message) {
        this.contentMessage = responseData.message;
        this.openPopupMessage();
      }
      if (!response.ok) {
        throw new Error(`HTTP error! status ${response.status}`);
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
.nes-btn-tour {
  color: black;
}

.nes-btn-tour:hover {
  color: white;
}


.center-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 75vh;
}
</style>