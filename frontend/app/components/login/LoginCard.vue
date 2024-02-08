<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})

  import { ref, onMounted } from 'vue';
  
  const client_id = import.meta.env.VITE_42INTRA_CLIENT_ID.split('"').join('');
  const redirect_uri = ref('');

  onMounted(() => {
    redirect_uri.value = encodeURIComponent(window.location.origin + "/endpoint/auth/callback");
  });

  const generateRandomString = () => {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  };

  const redirectToIntraLogin = () => {
    const url =`https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=${redirect_uri.value}&state=${generateRandomString()}&response_type=code`;
    window.location.href = url;
  };
</script>


<template>
  <div class="card card-size">
    <div class="card-header">Login / Register</div>
    <div class="card-body">
      <!-- ALERTS -->
      <div v-if="message" class="alert alert-success" role="alert">{{ message }}</div>
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
      <!-- LOGIN FORM -->
      <form v-if="isLoggedIn != 1 && !reg_form">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input v-model="username" @keyup.enter="$refs.loginpwfield.focus()" ref="loginnamefield" type="text" class="form-control" id="InputUsername" aria-describedby="usernameHelp">
        </div>
        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input v-model="password" @keyup.enter="$refs.loginbutton.focus()" ref="loginpwfield" type="password" class="form-control" id="InputPassword">
        </div>
        <div class="button-list">
          <button type="button" @keyup.enter="$refs.loginnamefield.focus()" ref="loginbutton" class="btn btn-primary" @click="login">Login</button>
          <a class="btn btn-link btn-sm" @click="reg_form = true; error = ''; message = ''">create account</a>
        </div>
      </form>
      <form v-if="isLoggedIn != 1 && !reg_form">
      <div class="button-list">
        Alternatively, 42 students can just log in with their intra accounts at 42. Just click on the magic button below
        <button type="button" ref="loginbutton_42intra" class="btn btn-primary" @click="redirectToIntraLogin">CLICK ME TO 42!</button>
      </div>
      </form>
      <!-- REGISTRATION FORM -->
      <form v-if="isLoggedIn == 0 && reg_form">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input v-model="username" @keyup.enter="$refs.regpwfield.focus()" ref="regnamefield" type="text" class="form-control" id="InputUsername" aria-describedby="usernameHelp">
        </div>
        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input v-model="password" @keyup.enter="$refs.regpw2field.focus()" ref="regpwfield" type="password" class="form-control" id="InputPassword">
        </div>
        <div class="mb-3">
          <label for="InputPassword2" class="form-label">Password (repeat)</label>
          <input v-model="password2" @keyup.enter="$refs.regbutton.focus()" ref="regpw2field" type="password" class="form-control" id="InputPassword2">
        </div>
        <div class="button-list">
          <button type="button" @keyup.enter="$refs.regnamefield.focus()" ref="regbutton" class="btn btn-primary" @click="register">Register</button>
          <a class="btn btn-link btn-sm" @click="reg_form = false; error = ''; message = ''">login</a>
        </div>
      </form>
      <!-- LOGGED IN -->
      <div v-if="isLoggedIn == 1">
        <div class="button-list">
          <button type="button" class="btn btn-primary" @click="logout">Logout</button>
        </div>
      </div>
      <!-- LOADING SPINNER -->
        <div v-if="isLoggedIn == 2" class="d-flex align-items-center justify-content-center shade-bg">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginCard',
    data() {
    return {
      username: '',
      password: '',
      password2: '',
      message: '',
      error: '',
      reg_form: false,
    }
  },
  methods: {
    async login() {
      isLoggedIn.value = 2
      this.message = ''
      this.error = ''
      try {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/api/userlogin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            'username': this.username,
            'password': this.password,
          })
        });
        const data = await response.json()
        if (response.status === 200) {
          isLoggedIn.value = 1
          this.password = ''
          this.message = data.message
          sessionStorage.setItem('userid',data.userid)
        } else if (response.status === 403 || response.status === 400) {
          isLoggedIn.value = 0 
          this.password = ''
          this.error = data.error
        }
      } catch (error) {
        console.error('Error:', error)
      }
    },
    async logout() {
      isLoggedIn.value = 2
      this.message = ''
      this.error = ''
      try {
        const response = await fetch('/endpoint/api/userlogout', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json()
        if (response.status === 200) {
          isLoggedIn.value = 0
          this.username = ''
          this.password = ''
          this.message = data.message
          sessionStorage.removeItem('userid');
        }
      } catch (error) {
        console.error('Error:', error)
      }
    },
    async register() {
      isLoggedIn.value = 2
      this.message = ''
      this.error = ''
      try {
        const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
        const response = await fetch('/endpoint/api/userregister', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
          },
          body: `username=${encodeURIComponent(this.username)}&password1=${encodeURIComponent(this.password)}&password2=${encodeURIComponent(this.password2)}`,
        });
        if (response.status === 200) {
          isLoggedIn.value = 1
          this.password = ''
          this.password2 = ''
          const data = await response.json()
          this.message = data.message
          sessionStorage.setItem('userid',data.userid);
        } else if (response.status === 403 || response.status === 400) {
          isLoggedIn.value = 0
          this.password = ''
          this.password2 = ''
          const data = await response.json()
          this.error = data.error
        }
      } catch (error) {
        console.error('Error:', error)
      }
    },
  }
}
</script>

<style>
  .card-size {
    min-width: px;
    max-width: 400px;
  }
  .button-list {
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .shade-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(255,255,255,0.7);
  }
</style>