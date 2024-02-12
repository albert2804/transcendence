<template>
    <div>
      <div class="centered-headings">
      <h1>You're on the local game site</h1>
      </div>
      <!-- Button to open the pop-up -->
      <button type="button" @click="openPopup">Open Popup</button>

      <!-- Conditionally render the Popup component -->
      <Popup v-if="isPopupOpen" @close="closePopup" />
      <div style="justify-content: center; margin-top: 20vh;">
        <LocalPong/>
      </div>
    </div>
  </template>

<!-- pages/index.vue -->

<script>
import Popup from '~/components/Popup.vue';

export default {
  components: {
    Popup,
  },
  data() {
    return {
      isPopupOpen: false,
    };
  },
  methods: {
    openPopup() {
      this.isPopupOpen = true;
    },
    closePopup() {
      this.isPopupOpen = false;
    },
  },
};
</script>
