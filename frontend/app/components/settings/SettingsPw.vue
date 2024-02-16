<template>
	<div v-if="openPopup" class="popup">
	<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
	 <div class="password_container">
		<div class="password">
			<label for="old_pw">Current Password:</label>
			<input type="password" id="old_pw" name="old_pw" v-model="old_pw">
		</div>
		<div class="password">
			<label for="password1">New Password:</label>
			<input type="password" id="password1" name="password1" v-model="password1">
		</div>
		<div class="password">
			<label for="password2">Confirm Password:</label>
			<input type="password" id="password2" name="password2" v-model="password2">
	 	</div>
		<div class="btn_password">
			<button type="button" class="btn btn-primary" @click="confirm">Confirm new password</button>
		</div>
	 </div>
	</div>
  </template>

  <script>
  export default{
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
					if (response.ok)
						console.log("Changed pw worked");
					else
						console.log("Changed pw didnt work:", response.status);

				} catch (error) {
					console.error('Error sending data to /endpoint/user/verify/:', error);
				}
			}
			else
				console.log("Passwords dont match");
		},

		closePopup() {
			this.$emit('close-popup');
		}
	},
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
.password_container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
	margin-bottom: 10px;
}
.password {
    margin-bottom: 10px;
}
</style>