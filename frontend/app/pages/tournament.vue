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
    <ErrorModal
      :isVisible="modalVisible"
      :content="modalContent"
      :modalTitle="'Response:'"
      modalId="ErrorModal"
      @hidden="resetModal"
    />
  </div>
</template>

<script>
import FormTournament from '~/components/tournament/FormTournament.vue';
import ListTournament from '~/components/tournament/ListTournament.vue';
import BracketsTournament from '~/components/tournament/BracketsTournament.vue';
import ErrorModal from '~/components/popup/ErrorMessages.vue';
import { ref } from 'vue';

export default {
  components: {FormTournament, ListTournament, ErrorModal}, 
  data() {
    return {
      formVisible: false,
      loggedInUser: "",
      recverror: '',
      recvmessage: '',
      modalContent: null,
      modalVisible: false,
      modalTitle: '',
      modalID: '',
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
        this.modalTitle = "Error";
      }
      else if (message) {
        console.log('print from parent', message);
        this.openModal(message);
        this.modalTitle = "Message";
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
      try {
        // Ensure Bootstrap is available globally
        this.modalContent = data;
        this.modalVisible = true;
        // this.$nextTick(() => {
        //   new bootstrap.Modal(document.getElementById('ErrorModal')).show();
        // });
        // if (typeof bootstrap !== 'undefined') {
        //   const myModalElement = document.getElementById('ErrorModal');
        //   const myModal = new bootstrap.Modal(myModalElement);

          // myModal.show();

          // myModal.addEventListener('shown.bs.modal', () => {
          //   // Your additional logic when the modal is shown
          // });

        // } else {
        //   console.error('Bootstrap is not available. Make sure it is properly included.');
        // }
      } catch (error) {
        console.error('Error opening modal:', error);
      }
    },

    resetModal() {
      this.modalVisible = false;
      this.modalContent = null;    
    }
  }
}
</script>