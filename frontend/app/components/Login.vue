<template>
  <div class="card">
    <div class="card-header">
      Login
    </div>
    <div class="card-body">
      <form v-if="!isLoggedIn">
        <div class="mb-3">
          <label for="InputUsername" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="InputUsername" aria-describedby="usernameHelp">
        </div>
        <div class="mb-3">
          <label for="InputPassword" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="InputPassword">
        </div>
        <button type="button" class="btn btn-primary" @click="login">Submit</button>
      </form>
      <div v-if="isLoggedIn">
        <p>You are logged in.</p>
        <button type="button" class="btn btn-primary" @click="logout">Logout</button>
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
      isLoggedIn: useCookie('isLoggedIn', { sameSite: 'strict' }).value,
    }
  },
  methods: {
    async login() {
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
        if (data.authenticated) {
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = true
          this.isLoggedIn = true
        } 
      } catch (error) {
        console.error('Error:', error)
      }
    },
    async logout() {
      try {
        const response = await fetch('/endpoint/api/userlogout', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json()
        if (!data.authenticated) {
          useCookie('isLoggedIn', { sameSite: 'strict' }).value = false
          this.isLoggedIn = false
        }
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }
}
</script>
