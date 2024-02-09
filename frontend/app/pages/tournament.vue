<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value;
  })
</script>

<template>
  <div>
    <div style="display: flex; flex-direction: column; align-items: center;">
      <h1>Youre on the tournament site</h1>
      <div v-if="isLoggedIn">
        <button @click="toggleForm" class="btn btn-primary">
        {{ formVisible ? 'No Tournament' : 'Create Tournament' }} </button>
      </div>
    </div>
    <div v-if="formVisible">
      <FormTournament v-bind:local="false"/>
    </div>
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
  },
}
</script>