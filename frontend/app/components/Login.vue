<template>
  <form>
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
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const csrfToken = useCookie('csrftoken').value
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
        console.log(data)
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }
}
</script>