<template>
  <div class="card">
    <div class="card-header">
      Login / Register
    </div>
    <div class="card-body">
      <!-- ALERTS -->
      <div v-if="message" class="alert alert-success" role="alert">
        {{ message }}
      </div>
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <!-- LOGIN FORM -->
      <form v-if="!isLoggedIn && !reg_form">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="InputUsername" aria-describedby="usernameHelp">
        </div>
        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="InputPassword">
        </div>
        <div style="display: flex; flex-direction: column; align-items: center;">
          <div>
            <button type="button" class="btn btn-primary" @click="login">Login</button>
          </div>
          <div>
            <a class="btn btn-link btn-sm" @click="reg_form = true; error = ''; message = ''">create account</a>
          </div>
        </div>
      </form>
      <!-- REGISTRATION FORM -->
      <form v-if="!isLoggedIn && reg_form">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="InputUsername" aria-describedby="usernameHelp">
        </div>
        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="InputPassword">
        </div>
        <div class="mb-3">
          <label for="InputPassword2" class="form-label">Password (repeat)</label>
          <input v-model="password2" type="password" class="form-control" id="InputPassword2">
        </div>
        <div style="display: flex; flex-direction: column; align-items: center;">
          <div>
            <button type="button" class="btn btn-primary" @click="register">Register</button>
          </div>
          <div>
            <a class="btn btn-link btn-sm" @click="reg_form = false; error = ''; message = ''">login</a>
          </div>
        </div>
      </form>
      <!-- LOGGED IN -->
      <div v-if="isLoggedIn">
        <!-- <p>You are logged in as {{ username }}</p> -->
        <button type="button" class="btn btn-primary" @click="logout">Logout</button>
      </div>
      <div v-if="wait">
        <div v-if="wait" class="d-flex align-items-center justify-content-center" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background: rgba(255,255,255,0.7);">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      wait: false,
      message: '',
      error: '',
      reg_form: false,
      isLoggedIn: useCookie('isLoggedIn', { sameSite: 'strict' }).value,
    }
  },
  methods: {
    async login() {
      this.wait = true
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
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = true
          this.password = ''
          this.isLoggedIn = true
          this.message = data.message
        } else if (response.status === 403 || response.status === 400) {
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = false
          this.password = ''
          this.isLoggedIn = false
          this.error = data.error
        }
        this.wait = false
      } catch (error) {
        this.wait = false
        console.error('Error:', error)
      }
    },
    async logout() {
      this.wait = true
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
        this.wait = false
        if (response.status === 200) {
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = false
          this.isLoggedIn = false
          this.username = ''
          this.password = ''
          this.message = data.message
        }
      } catch (error) {
        this.wait = false
        console.error('Error:', error)
      }
    },
    async register() {
      this.wait = true
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
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = true
          this.password = ''
          this.password2 = ''
          this.isLoggedIn = true
          const data = await response.json()
          this.message = data.message
        } else if (response.status === 403 || response.status === 400) {
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = false
          this.password = ''
          this.password2 = ''
          this.isLoggedIn = false
          const data = await response.json()
          this.error = data.error
        }
        this.wait = false
      } catch (error) {
        this.wait = false
        console.error('Error:', error)
      }
    },
  }
}
</script>
