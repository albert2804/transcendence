<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn, userName, userId} from '~/store';
  watchEffect(() => {
	isLoggedIn.value = isLoggedIn.value
	userName.value = userName.value
	userId.value = userId.value
  })

  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  const client_id = import.meta.env.VITE_42INTRA_CLIENT_ID.split('"').join('');
  const redirect_uri = ref('');
  const route = useRoute();
  const router = useRouter();
  const message = ref('');
  const error = ref('');
  const qmessage = ref('');
  const qerror = ref('');
  const username = ref('');
  const password = ref('');
  const password2 = ref('');
  const reg_form = ref(false);

  onMounted(() => {
    redirect_uri.value = encodeURIComponent(window.location.origin + "/endpoint/auth/callback");
    qerror.value = route.query.error;
    qmessage.value = route.query.message;

    router.replace({ path: route.path });
  });
  const login = async () => 
  {
    isLoggedIn.value = 2 // Store
    message.value = ''
    message.error = ''
    qerror.value = ''
    try {
      const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
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
      const data = await response.json()
      if (response.status === 200) {
        isLoggedIn.value = 1 // Store
		userName.value = data.username // Store
		userId.value = data.userid // Store
        password.value = ''
        error.value = ''
        message.value = data.message
        sessionStorage.setItem('userid',data.userid)
      } else if (response.status === 403 || response.status === 400) {
        isLoggedIn.value = 0 // Store
		userName.value = '' // Store
		userId.value = '' // Store
        password.value = ''
        message.value=''
        error.value = data.error
      }
      } catch (error) {
        console.error('Error:', error)
      }
  };

  const logout = async () => {
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
      isLoggedIn.value = 0; //Store
	  userName.value = ''; // Store
	  userId.value = ''; // Store   
      username.value = '';
      password.value = '';
      message.value = data.message;
      sessionStorage.removeItem('userid');
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

const register = async () => {
  isLoggedIn.value = 2; // Store
  message.value = '';
  error.value = '';
  try {
    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
    const response = await fetch('/endpoint/api/userregister', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      body: `username=${encodeURIComponent(username.value)}&password1=${encodeURIComponent(password.value)}&password2=${encodeURIComponent(password2.value)}&alias=${encodeURIComponent(username.value)}`,
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
      sessionStorage.setItem('userid', data.userid);
    } else if (response.status === 403 || response.status === 400) {
      isLoggedIn.value = 0; // Store
	  userName.value = ''; // Store
	  userId.value = ''; // Store
      password.value = '';
      password2.value = '';
      const data = await response.json();
      message.value='';
      error.value = data.error;
    }
  } catch (error) {
    console.error('Error:', error);
  }};

  const generateRandomString = () => {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  };

  const redirectToIntraLogin = () => {
    const url =`https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=${redirect_uri.value}&state=${generateRandomString()}&response_type=code`;
    window.location.href = url;
  };
  
  const redirectToHomePage =() => {
    const url =`https://localhost`;
    window.location.href = url;
  }

</script>


<template>
  <section class="nes-container container-fluid with-title vw-50 automargin" style="max-width: 30vw; min-width: 23em">
    <p class="title" v-if="isLoggedIn!=1 && !reg_form">Login</p>
    <p class="title" v-if="isLoggedIn == 0 && reg_form">Register</p>
    <div class="card-body">
      <!-- ALERTS -->
      <div v-if="message" class="alert alert-success" style="min-width: 14em" role="alert">{{ message }}</div>
      <div v-if="qmessage" class="alert alert-success" style="min-width: 14em" role="alert">{{ qmessage }}</div>
      <div v-if="error" class="alert alert-danger" style="min-width: 14em" role="alert">{{ error }}</div>
      <div v-if="qerror" class="alert alert-danger" style="min-width: 14em" role="alert">{{ qerror }}</div>
      <!-- LOGIN FORM -->
      <form v-if="isLoggedIn != 1 && !reg_form">
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
          <a class="nes-btn btn-primary btn-sm" @click="reg_form = true; error = ''; message = ''">create account</a>
        </div>
      </form>
      <form v-if="isLoggedIn != 1 && !reg_form">
        <p> Alternatively, 42 students can log in with their 42 intra accounts.<br> Just click on the magic button below.</p>
      <div class="button-list">
        <button type="button" ref="loginbutton_42intra" class="btn nes-btn" @click="redirectToIntraLogin">CLICK ME TO 42!</button>
      </div>
      </form>
      <!-- REGISTRATION FORM -->
      <form v-if="isLoggedIn == 0 && reg_form">
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
      <div v-if="isLoggedIn == 1">
        <div class="button-list">
          <button type="button" class="btn nes-btn btn-primary" @click="logout">Logout</button>
        </div>
      </div>
      <!-- LOADING SPINNER -->
        <div v-if="isLoggedIn == 2" class="d-flex align-items-center justify-content-center shade-bg">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
    </div>
  </section>
</template>

<!-- <script>
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
          body: `username=${encodeURIComponent(this.username)}&password1=${encodeURIComponent(this.password)}&password2=${encodeURIComponent(this.password2)}&alias=${encodeURIComponent(this.username)}`,
        });
        if (response.status === 200) {
          
          isLoggedIn.value = 1
          this.password = ''
          this.password2 = ''
          const data = await response.json()
          this.message = data.message
          sessionStorage.setItem('userid',data.userid);
          window.location.href = 'https://localhost';
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
</script> -->

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