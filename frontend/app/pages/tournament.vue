<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value;
  })
</script>

<template>
  <div>
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20vh;">
      <h1>Youre on the tournament site</h1>
      <div v-if="isLoggedIn === 1">
        <button type="button" class="btn btn-primary" @click="createTournament">Create Tournament</button>
        <div v-if="tournamentCreation">
          <FormTournament/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FormTournament from '../components/tournament/FormTournament.vue';
export default {
  components: { FormTournament },
  data() {
    return {
      tournamentCreation: false,
    };
  },
  methods: {
    createTournament() {
      this.tournamentCreation = !this.tournamentCreation
    },
  },
}
</script>