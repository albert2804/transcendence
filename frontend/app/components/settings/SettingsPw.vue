<template>
	<div v-if="openPopup" class="popup">
		<div class="password_container">
			<div class="password nes-field">
				<label for="old_pw">Current Password</label>
				<input class="nes-input" type="password" id="old_pw" name="old_pw" v-model="old_pw">
			</div>
			<div class="password nes-field">
				<label for="password1">New Password</label>
				<input class="nes-input" type="password" id="password1" name="password1" v-model="password1">
			</div>
			<div class="password nes-field">
				<label for="password2">Confirm Password</label>
				<input class="nes-input" type="password" id="password2" name="password2" v-model="password2">
			</div>
			<div class="nes-btn nes-btn-pw is-success nav-item" @click="confirm">Confirm new password
				
			</div>
		</div>
		<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
	</div>
  </template>

  <script>
  import { isLoggedIn, userName, userId } from '~/store';

  export default{

	watch: {
    isLoggedIn: {
      immediate: true,
      handler(newValue) {
        this.loginStatus = newValue;
      }
    },
  },

	props: {
    openPopup: Boolean
  },
	data(){
		return {
			old_pw: '',
			password1:'',
			password2:'',
			error: '',
		};
	},

	methods: {
		async confirm() {
		  if (this.password1 === this.password2) {
			  try {
				  const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
				  const response = await fetch('/endpoint/user/verify/', {
					  method: 'POST',
					  headers: {
						  'Content-Type': 'application/json',
						  'X-CSRFToken': csrfToken,
						}, 
						body: JSON.stringify({
						old_pw: encodeURIComponent(this.old_pw),
						password1: encodeURIComponent(this.password1),
						password2: encodeURIComponent(this.password2)})
					})
					const data = await response.json();
					this.closePopup();
					this.error = data.error;
					this.message = data.status;
					this.sendMessagetoParent(this.message, this.error);
					if (response.status === 200){
						isLoggedIn.value = 0; // Store
						userName.value = ''; // Store
						userId.value = ''; // Store
						await fetch('/endpoint/api/userlogout');
						this.$router.push('/login');
					}
				} catch (error) {
					console.error('Error sending data to /endpoint/user/verify/:', error);
				}
			}
			else {
				console.log("Passwords dont match");
				this.sendMessagetoParent('', 'Passwords dont match');
				this.closePopup();
			}
		},

		closePopup() {
			this.$emit('close-popup');
		},

		sendMessagetoParent(message, error) {
			this.$emit('message-from-child', message, error);
		}
	},
}
</script>

<style>

.password_container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
	margin-bottom: 100px;
}

.password {
    margin-bottom: 10px;
}

.nes-btn-pw{
    min-width: 15%;
    color: #000000;
    margin-right: 1%;
  }
  .nes-btn-pw:hover{
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

  .popup {
	display: flex;
}

.btn-close {
	align-items: flex-end;
}

</style>