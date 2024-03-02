<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
  <div class="d-flex flex-column">
    <div class="nes-container container-fluid with-title automargin" style="text-align: left;">
      <p class="title">User profile</p>
      <div class="user-info-container">
        <div v-if="isLoggedIn === 1" class="col user-info-container">
          <UserProfilePic />
        </div>
        <div v-if="isLoggedIn === 1" class="col user-info-container">
          <UserInfo />
        </div>
        <div v-else>
          <h4>No user statistics available. Please log in to view user profiles.</h4>
        </div>
      </div>
    </div>
    <div class="nes-container container-fluid with-title vw-50 automargin" style="text-align: left;">
      <div v-if="isLoggedIn === 1" class="user-games-history">
        <UserGameHistory />
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
.user-games-history {
  max-width: 580px; /* Set the maximum width to 580px */
  width: 100%;
}

/* Adjust table width and column width */
.user-games-history table {
  width: 100%; /* Make the table fill its container */
}

.user-games-history th,
.user-games-history td {
  padding: 8px; /* Adjust cell padding */
  max-width: 100px; /* Set maximum width for cells */
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis; /* Add ellipsis for overflow text */
  white-space: nowrap; /* Prevent text wrapping */
}

@media screen and (max-width: 1575px) {
  .user-games-history {
    display: none;
  }
}

@media screen and (max-width: 700px) {
  .user-info-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>