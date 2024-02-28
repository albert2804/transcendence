<template>
  <div class="nes-container vh-5" style="background-color:#f8f9fa; width: 98%; justify-content: center; margin: 0 auto;">
    <GameModal modalId="pongmodal" />
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#pongNavbar" 
      data-target="#pongNavbar" aria-controls="pongNavbar" aria-expanded="false" aria-label="Toggle navigation"
      style="width: 100%; border: none;">
        <span style="color: black; float:left;">MENU</span>
        <span style="color: black;">MENU</span>
        <span style="color: black; float:right;">MENU</span>
        <progress class="nes-progress is-pattern" value="100" max="100"></progress>
      </button>
        <div class="collapse navbar-collapse justify-content-center" id="pongNavbar">
              <NuxtLink class="nes-btn is-success nav-item" to="/">Home</NuxtLink>
              <NuxtLink class="nes-btn is-warning nav-item" to="/tournament">Tournament</NuxtLink>
              <NuxtLink class="nes-btn is-error nav-item" to="/leaderboard">Leaderboard</NuxtLink>
              <NuxtLink v-if="!loginStatus" class="nes-btn is-error nav-item" to="/login">Login</NuxtLink>
              <button v-if="loginStatus" class="nes-btn is-error nav-item" @click="reloadUserProfile">UserProfile</button>
              <NuxtLink v-if="loginStatus" class="nes-btn is-error nav-item" to="/login">Logout</NuxtLink>
        </div>
    </nav>
  </div>
</template>

<script>
import { isLoggedIn, userName } from '~/store';
export default {
  name: 'NavBar',
  data() {
    return {
      loginStatus: isLoggedIn,
      userName: userName,
    }
  },
  watch: {
    loginStatus: {
      immediate: true,
      handler(newValue) {
        isLoggedIn.value = newValue;
      }
    },
    userName: {
      immediate: true,
      handler(newValue) {
        userName.value = newValue;
      }
    }
  },
  methods: {
    reloadUserProfile() {
      this.$router.push(`/userinfopage?username=${this.userName}`).then(() => {
      this.$router.go();
      });
    },
  }
}
</script>

<style scoped>
  .nes-btn{
    min-width: 15%;
    color: #000000;
    margin-right: 1%;
    overflow: hidden;

  }
  .nes-btn:hover{
    color: #ffffff;
  }

  .nes-progress{
    position: relative;
    top: 0;
    transition: linear 0.1s;
  }
  .nes-progress:hover{
    top: -3px
  }

  .nes-navbar{
    color: black;
  }
</style>