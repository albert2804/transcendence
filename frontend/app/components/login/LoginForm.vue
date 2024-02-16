<template>
	<div class="container-fluid vh-100">
	  <form @submit.prevent="submitData" id="loginForm">
		<h2>Login</h2>
		<label for="username">Username:</label>
		<input type="text" id="username" v-model="username" required><br><br>
		<label for="password">Password:</label>
		<input type="password" id="password" v-model="password" required><br><br>
		<button type="submit">Login</button>
	  </form>
	  <h2>Not registered?</h2>
	  <button type="button" @click="register">Register</button>
	</div>
  </template>
  
  <script>
  export default {
	data() {
	  return {
		username: '',
		password: ''
	  };
	},
	methods: {
	  async submitData() {
		try {
		  const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
		  console.log('CSRF Token:', token); 
		  const formData = new FormData();
		  formData.append('username', this.username);
		  formData.append('password', this.password);
  
		  const response = await fetch('http://localhost/endpoint/session/checkUser', {
			method: 'POST',
			body: formData,
			headers: {
			  'X-CSRFToken': token
			}
		  });
  
		  console.log("Sent", response); // Handle the response as needed
		} catch (error) {
		  console.error('Not Sent', error); // Handle errors
		}
	  }
	}
  };
  </script>
  