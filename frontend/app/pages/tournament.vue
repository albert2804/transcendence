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
      <h1 style="margin-top: 20px;">Youre on the tournament site</h1>
      <button @click="callSignUp" class="nes-btn is-primary"></button>
      <div v-if="isLoggedIn">
        <button type="button" @click="toggleForm" class="nes-btn is-primary" style="margin-top: 20px;">
        {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
      </div>
    </div>
    <div class="ErrorHandling">
      <div v-if="recvmessage" class="alert alert-success" style="min-width: 14em; margin-bottom: 20px; margin-top: 20px;" role="alert">{{ recvmessage }}</div>
      <div v-if="recverror" class="alert alert-danger" style="min-width: 14em; margin-bottom: 20px; margin-top: 20px;" role="alert">{{ recverror }}</div>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false" :loggedInUser="loggedInUser" @message-from-child="handleUpdate"/>
    </div>
    <div v-if="isLoggedIn">
      <ListTournament :loggedInUser="loggedInUser" @message-from-child="handleUpdate"/>
    </div>
    <ErrorModal v-show="modalContent" :content="modalContent" :modalTitle="'Response:'" modalId="exampleModal" ariaLabel="Modal for errors and messages" />
  </div>
</template>

<script>
import FormTournament from '~/components/tournament/FormTournament.vue';
import ListTournament from '~/components/tournament/ListTournament.vue';
import BracketsTournament from '~/components/tournament/BracketsTournament.vue';
import ErrorModal from '~/components/popup/ErrorMessages.vue';

export default {
  components: {FormTournament, ListTournament, ErrorModal}, 
  data() {
    return {
      formVisible: false,
      loggedInUser: "",
      recverror: '',
      recvmessage: '',
      modalContent: null,
    };
  },
  setup() {
    const handleUpdate = ref(false);
    let recvmessage = ref('');
    let recverror = ref('');

    return {
      error,
      message,
    }
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
      if (!response.ok) {
        throw new Error(`HTTP error! status ${response.status}`);
      }
    },
    async handleUpdate(message, error) {
      this.recverror = error;
      this.recvmessage = message;
      if (error) {
        console.log('print from parent', error);
        this.openModal(error);
      }
      else if (message) {
        console.log('print from parent', message);
        this.openModal(message);
      }
      this.$forceUpdate();
      this.resetMessages();
    },
    async resetMessages() {
      await new Promise(resolve => setTimeout(resolve, 5000));
      this.recverror = '';
      this.recvmessage = '';
      // this.$forceUpdate();
    },
    async openModal(data) {
      const myModal = document.getElementById('ErrorModal').show();
    // const myInput = document.getElementById('myInput')

      myModal.addEventListener('shown.bs.modal', () => {
      //  myInput.focus()
      })
      this.modalContent = data;
    },
    resetModal() {
      this.modalContent = null;    
    }
  }
}
</script>