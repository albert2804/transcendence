<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
	<div class="pic">
	  <div v-if="pic">
		<p>Username: {{ userStats.username }}</p>
	  </div>
	  <div v-else>
		<p>Loading failure for Profile Pic</p>
	  </div>
	</div>
  </template>