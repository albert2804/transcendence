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
      <div v-if="isLoggedIn">
        <button @click="toggleForm" class="btn btn-primary">
        {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
      </div>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false"/>
    </div>
    <button @click="callSignUp" class="btn btn-primary"></button>
  </div>
</template>

<script>
import FormTournament from '~/components/tournament/FormTournament.vue';

export default {
  components: 'FormTournament',
  data() {
    return {
      formVisible: false,
    };
  },
  methods: {
    toggleForm() {
      this.formVisible = !this.formVisible
    },
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