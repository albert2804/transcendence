<template>
	<div v-if="openPopup" class="popup">
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
			<div class="nes-btn is-success nav-item" @click="confirm">Confirm new password
				
			</div>
		</div>
		<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
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
					if (response.ok){
						
						this.closePopup();
						await this.$router.push('/login');
						location.reload();
						console.log("Changed pw worked");
					}
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

.password_container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
	margin-bottom: 100px;
}

.password {
    margin-bottom: 10px;
}

.nes-btn{
    min-width: 15%;
    color: #000000;
    margin-right: 1%;
    overflow: hidden;
  }
  .nes-btn:hover{
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