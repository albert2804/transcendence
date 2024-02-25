<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-80">
    <div class="nes-container container-fluid with-title vw-50 automargin" style="text-align: left; min-width: 580px;">
      <p class="title">User profile</p>
      <div style="display: flex; align-items: center">
        <div v-if="isLoggedIn === 1" class="user-info-container">
          <div class="col">
            <UserProfilePic />
          </div>
          <div class="col">
            <UserInfo />
            <UserGameHistory />
          </div>
        </div>
        <div v-else>
          <h4>No user statistics available. Please log in to view user profiles.</h4>
        </div>
      </div>
    </div>
  </div>
</template>

  <script>
  export default {
  };
</script>

<style scoped>
  .user-info-container {
    display: flex;
    align-items: center; 
    justify-content: center;
    width: 100%;
  }
</style>