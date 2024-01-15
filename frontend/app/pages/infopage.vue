<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
    <div>
      <div style="display: flex; justify-content: center; margin-top: 20vh;">
        <div v-if="isLoggedIn === 1">
          <InfoComponent />
          <ProfilePic />
        </div>
        <div v-else>
          <p>No user statistics available.</p>
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
  };
</script>