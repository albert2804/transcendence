<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
    <div class="container-fluid vh-100">
      <div style="display: flex; justify-content: center; margin-top: 20vh;">
        <div v-if="isLoggedIn === 1">
          <UserInfo />
          <UserProfilePic />
        </div>
        <div v-else>
          <h2>No user statistics available.</h2>
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
  };
</script>

