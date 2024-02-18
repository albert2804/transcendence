<!-- https://getbootstrap.com/docs/5.3/components/navbar/ -->
<script setup>
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value
  })
</script>

<template>
<div class="nes-container vh-5" style="height: 10vh; position: absolute; bottom: 2%; width: 98%">
    <GameModal modalId="pongmodal" ariaLabel="A modal to play our remote Pong Game" />
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <!-- <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#pongNavbar" aria-controls="pongNavbar" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button> -->
        <div class="collapse navbar-collapse" id="pongNavbar">
              <NuxtLink class="nes-btn is-primary" v-if="isLoggedIn != 1" to="/login">Login</NuxtLink>
              <NuxtLink class="nes-btn is-primary" v-if="isLoggedIn === 1" to="/login">Logout</NuxtLink>
              <NuxtLink class="nes-btn is-success" to="/">Home</NuxtLink>
              <NuxtLink class="nes-btn is-warning" @click="showGameModal" style="cursor: pointer;">Play</NuxtLink>
              <NuxtLink class="nes-btn is-warning" to="/tournament">Tournament</NuxtLink>
              <NuxtLink class="nes-btn is-error" to="/leaderboard">Leaderboard</NuxtLink>
              <NuxtLink class="nes-btn is-error" to="/userinfopage">User Profile</NuxtLink>
        </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    showGameModal() {
      this.$nextTick(() => {
        new bootstrap.Modal(document.getElementById('pongmodal')).show();
      });
    },
  },
}
</script>

<style scoped>
  .nes-btn{
    width: 16%;
    color: #000000;
    margin-right: 1%
  }
  .nes-btn:focus{
    color: #ffffff;
  }
</style>