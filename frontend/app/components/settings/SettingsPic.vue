<template>
	<div v-if="openPopup" class="popup">
	<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
	<div class="profilepic_container">
	  <div v-if="userProfilePic">
		<img :src=userProfilePic.url alt="Profile Picture">
	  </div>
	  <div v-else>
		<p>Loading failure for Profile Pic</p>
	  </div>
	  <div class="btn_profilepic">
		<input type="file" ref="fileInput" style="display: none;" @change="changeProfilePicture">
		<button type="button" class="btn btn-primary" @click="selectProfilePicture">Change Profile Picture</button>
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
			error: '',
		};
	},

	mounted() {
		this.fetch_picture();
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
			if (response.ok){
				this.closePopup();
				location.reload();
			}
			} catch (error) {
				console.error('Error sending picture to backend', error);
			}
		},
		
		closePopup() {
			this.fetch_picture();
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
  .profilepic_container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 10px;
}

  .btn_profilepic {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 10px;
}
</style>