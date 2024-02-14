<template>
	<div v-if="openPopup" class="popup">
	<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
	 <div class="password_container">
		<div class="password">
			<label for="old_password">Current Password:</label>
			<input type="password" id="old_password" name="old_password">
		</div>
		<div class="password">
			<label for="new_password">New Password:</label>
			<input type="password" id="new_password" name="new_password">
		</div>
		<div class="password">
			<label for="confirm_password">Confirm Password:</label>
			<input type="password" id="confirm_password" name="confirm_password">
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
			userProfilePic: '{}',
			editedName: '',
			originalName: '',
			nameResponse: null,
			error: '',
		};
	},

	mounted() {
		this.fetch_picture();
		this.fetch_name();
	},

	methods: {
		async fetch_picture() {
		  try {
		    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const response = await fetch('/endpoint/user/profilepic/', {
        		method: 'GET',
          		headers: {
            	'Content-Type': 'application/json',
            	'X-CSRFToken': csrfToken,
          	    }
       		 })
			this.userProfilePic = await response.json();
			} catch (error) {
				console.error('Error fetching user profile pic:', error);
			}
		},

		async selectProfilePicture() {
     	 try {
        	const fileInput = this.$refs.fileInput;
        	fileInput.click(); // Trigger file input click event
      	} catch (error) {
       	 console.error('Error selecting picture:', error);
      	}
    	},

		async changeProfilePicture (event) {
			try {
				const fileInput = event.target;
				this.newPic = fileInput.files[0];
	
				if (!this.newPic) {
					  console.error('No file selected.');
				  return;
					}
				} catch(error) {
					console.error('Error selecting Picture:', error);
				}

			try {
				const formData = new FormData();
				formData.append('newPic', this.newPic);
				for (const entry of formData.entries()) {
					console.log(entry[0], entry[1]);
				}
				const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
				const response = await fetch('/endpoint/user/profilepic/', {
        			method: 'POST',
          			headers: {
            		'X-CSRFToken': csrfToken,
          	    	},
					body: formData
       		 	});
			if (response.ok)
				await this.fetch_picture();
			} catch (error) {
				console.error('Error sending picture to backend', error);
			}
		},

		async fetch_name() {
		  try {
		    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const response = await fetch('/endpoint/user/info/', {
        		method: 'GET',
          		headers: {
            	'Content-Type': 'application/json',
            	'X-CSRFToken': csrfToken,
          	    }
       		 })
			this.nameResponse = await response.json();
			if (response.ok) {
				this.originalName = this.nameResponse.username;
				this.editedName = this.originalName;
				}
			} catch (error) {
				console.error('Error fetching user alias:', error);
			}
		},

		async saveChanges() {
			try {
		    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const response = await fetch('/endpoint/user/info/', {
        		method: 'POST',
          		headers: {
            	'Content-Type': 'application/json',
            	'X-CSRFToken': csrfToken,
          	    },
				body: JSON.stringify({ newUsername: this.editedName })
       		 })
			 if (response.ok)
			 	console.log("Changed username worked");
			} catch (error) {
				console.error('Error updating user alias:', error);
			}
		},
		
		cancelChanges() {
			this.fetch_name();
     		this.editedName = this.originalName;
    	},
		
		confirm() {
			
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