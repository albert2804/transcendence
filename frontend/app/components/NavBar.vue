<template>
  <div class="nes-container" style="background-color:#f8f9fa; width: 98%; justify-content: center; padding: 0; margin: auto;">
    <GameModal modalId="pongmodal" />
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#pongNavbar" data-target="#pongNavbar" aria-controls="pongNavbar" aria-expanded="false" aria-label="Toggle navigation" style="width: 100%; border: none; justify-content: center;">
        <span style="color: black; font-size: 1rem;">MENU</span>
        <progress class="nes-progress is-pattern" value="100" max="100"></progress>
      </button>
      <div class="collapse navbar-collapse" id="pongNavbar" style="width:100%; padding: 2vh 2vw 1vh 2vw;">
        <NuxtLink class="nes-btn nes-btn-style is-success nav-item" to="/">Home</NuxtLink>
        <NuxtLink v-if="loginStatus" class="nes-btn nes-btn-style is-success nav-item" to="/tournament">Tournament</NuxtLink>
        <NuxtLink class="nes-btn nes-btn-style is-warning nav-item" to="/leaderboard">Leaderboard</NuxtLink>
        <NuxtLink v-if="loginStatus" class="nes-btn nes-btn-style is-error nav-item" to="/userinfopage">UserProfile</NuxtLink>
        <NuxtLink v-if="!loginStatus" class="nes-btn nes-btn-style is-error nav-item" to="/login">Login</NuxtLink>
        <NuxtLink v-if="loginStatus" class="nes-btn nes-btn-style is-error nav-item" to="/login">Logout</NuxtLink>
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
    isLoggedIn: {
      immediate: true,
      handler(newValue) {
        this.loginStatus = newValue;
      }
    },
    userName: {
      immediate: true,
      handler(newValue) {
        userName.value = newValue;
      }
    }
  },
}
</script>

<style scoped>
  .nav-item{
	width: 100%;
	height: 3.5vh;
  }
  .nes-btn-style{
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    color: black;
    margin-bottom: 1vh;
    margin-right: 0.3vw;
    margin-left: 0.3vw;
  }
  .nes-btn-style:hover{
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