<template>
	<section class="nes-container container-fluid with-title automargin main resp-font-size">
		<p class="title" style="z-index: 100;" v-if="loginStatus!=1 && !reg_form">Login</p>
		<p class="title" style="z-index: 100;" v-if="loginStatus == 0 && reg_form">Register</p>
		<div class="card-body" style="font-size: 1rem;">
		<!-- ALERTS -->
		<div v-if="message" class="alert alert-success" role="alert">{{ message }}</div>
		<div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
		<!-- LOGIN FORM -->
		<form v-if="loginStatus != 1 && !reg_form">
			<div class="nes-field mb-3">
			<label for="InputUsername" class="form-label">Username</label>
			<input v-model="username" @keyup.enter="$refs.loginpwfield.focus()" ref="loginnamefield" type="text" class="form-control nes-input" id="InputUsername" aria-describedby="usernameHelp">
			</div>
			<div class="nes-field mb-3">
			<label for="InputPassword" class="form-label">Password</label>
			<input v-model="password" @keyup.enter="$refs.loginbutton.focus()" ref="loginpwfield" type="password" class="form-control nes-input" id="InputPassword">
			</div>
			<div class="button-list">
			<button type="button" @keyup.enter="$refs.loginnamefield.focus()" ref="loginbutton" class="btn nes-btn btn-primary" @click="login">Login</button>
      <div style="height: 10px;"></div>
			<a class="nes-btn btn-primary btn-sm" @click="reg_form = true; error = ''; message = ''">create account</a>
			</div>
		</form>
		<form v-if="loginStatus != 1 && !reg_form">
      <div style="height: 10px;"></div>
      <p style="overflow:hidden"> Alternatively, 42 students can log in with their 42 intra accounts.<br> Just click on the magic button below.</p>
		<div class="button-list">
			<button type="button" ref="loginbutton_42intra" class="btn nes-btn" @click="redirectToIntraLogin">CLICK ME TO 42!</button>
		</div>
		</form>
		<!-- REGISTRATION FORM -->
		<form v-if="loginStatus == 0 && reg_form">
			<div class="nes-field mb-3">
			<label for="InputUsername" class="form-label">Username</label>
			<input v-model="username" @keyup.enter="$refs.regpwfield.focus()" ref="regnamefield" type="text" class="form-control nes-input" id="InputUsername" aria-describedby="usernameHelp">
			</div>
			<div class="nes-field mb-3">
			<label for="InputPassword" class="form-label">Password</label>
			<input v-model="password" @keyup.enter="$refs.regpw2field.focus()" ref="regpwfield" type="password" class="form-control nes-input" id="InputPassword">
			</div>
			<div class="nes-field mb-3">
			<label for="InputPassword2" class="form-label">Password (repeat)</label>
			<input v-model="password2" @keyup.enter="$refs.regbutton.focus()" ref="regpw2field" type="password" class="form-control nes-input" id="InputPassword2">
			</div>
			<div class="button-list">
			<button type="button" @keyup.enter="$refs.regnamefield.focus()" ref="regbutton" class="btn nes-btn btn-primary" @click="register">Register</button>
			<a class="btn nes-btn btn-link btn-sm" @click="reg_form = false; error = ''; message = ''">login</a>
			</div>
		</form>
		<!-- LOGGED IN -->
		<div v-if="loginStatus == 1">
			<div class="button-list">
			<button type="button" class="btn nes-btn btn-primary" @click="logout">Logout</button>
			</div>
		</div>
		<!-- LOADING SPINNER -->
    <div v-if="loginStatus == 2 || loginStatus == undefined" class="d-flex align-items-center justify-content-center shade-bg">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
		</div>
	</section>
</template>

<script>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { isLoggedIn, userName, userId} from '~/store';

  export default {
    name: 'LoginCard',
    setup() {
      const client_id = import.meta.env.VITE_42INTRA_CLIENT_ID.split('"').join('');
      const redirect_uri = ref('');
      const route = useRoute();
      const router = useRouter();
      const message = ref('');
      const error = ref('');
      const username = ref('');
      const password = ref('');
      const password2 = ref('');
      const reg_form = ref(false);
      const loginStatus = ref(isLoggedIn.value);

      // watch effect
      watchEffect(() => {
        loginStatus.value = isLoggedIn.value;
      });
      // 
      onMounted(() => {
        redirect_uri.value = encodeURIComponent(window.location.origin + "/endpoint/auth/callback");
        if (route.query.error) {
          error.value = route.query.error;
        }
        if (route.query.message) {
          message.value = route.query.message;
        }

        router.replace({ path: route.path });
      });
      // login
      async function login() {
        isLoggedIn.value = 2; // Store
        message.value = '';
        error.value = '';
        try {
          const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
          const response = await fetch('/endpoint/api/userlogin', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
              'username': username.value,
              'password': password.value,
            })
          });
          const data = await response.json();
          if (response.status === 200) {
            isLoggedIn.value = 1; // Store
            userName.value = data.username; // Store
            userId.value = data.userid; // Store
            password.value = '';
            error.value = '';
            message.value = data.message;
          } else if (response.status === 403 || response.status === 400) {
            isLoggedIn.value = 0; // Store
            userName.value = ''; // Store
            userId.value = ''; // Store
            password.value = '';
            message.value = '';
            error.value = data.error;
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
      // logout
      async function logout() {
        isLoggedIn.value = 2; // Store
        message.value = '';
        error.value = '';
        try {
          const response = await fetch('/endpoint/api/userlogout', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const data = await response.json();
          if (response.status === 200) {
            isLoggedIn.value = 0; // Store
            userName.value = ''; // Store
            userId.value = ''; // Store
            username.value = '';
            password.value = '';
            message.value = data.message;
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
      // register
      async function register() {
        isLoggedIn.value = 2; // Store
        message.value = '';
        error.value = '';
        try {
          const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
          const response = await fetch('/endpoint/api/userregister', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
              'username': username.value,
              'password1': password.value,
              'password2': password2.value,
            })
          });
          if (response.status === 200) {
            const data = await response.json();
            isLoggedIn.value = 1; // Store
            userName.value = data.username; // Store
            userId.value = data.userid; // Store
            password.value = '';
            password2.value = '';
            error.value = '';
            message.value = data.message;
          } else if (response.status === 403 || response.status === 400) {
            isLoggedIn.value = 0; // Store
            userName.value = ''; // Store
            userId.value = ''; // Store
            password.value = '';
            password2.value = '';
            const data = await response.json();
            message.value = '';
            error.value = data.error;
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
      // Stuff for 42 intra login
      function generateRandomString() {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      }
      function redirectToIntraLogin() {
        message.value = '';
        error.value = '';
        const url = `https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=${redirect_uri.value}&state=${generateRandomString()}&response_type=code`;
        window.location.href = url;
      }
      function redirectToHomePage() {
        const url = `https://localhost`;
        window.location
      }
      return {
        client_id,
        redirect_uri,
        route,
        router,
        message,
        error,
        username,
        password,
        password2,
        reg_form,
        loginStatus,
        login,
        logout,
        register,
        redirectToIntraLogin,
        redirectToHomePage,
      };
    }
  }
</script>

<style>

.main {
  max-width: 500px; 
  word-wrap: break-word;
}

@media screen and (max-width: 850px) {
  .main {
    max-width: 80vw;
  }
}

@media screen and (max-width: 850px) {
  .main * {
    font-size: 0.8rem;
  }
}

</style>