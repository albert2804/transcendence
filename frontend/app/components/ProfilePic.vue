<template>
	<div class="profilepic">
	  <div v-if="userProfilePic">
		<img :src=userProfilePic.url alt="Profile Picture">
	  </div>
	  <div v-else>
		<p>Loading failure for Profile Pic</p>
	  </div>
	  
	  <div>
      <input type="file" ref="fileInput" @change="uploadProfilePic" />
      <button @click="changeProfilePicture">Change</button>
  	 </div>
	</div>
  </template>

<script>
	import { useRoute } from 'vue-router';
	export default{
	data(){
		return {
			userProfilePic: '',
		};
	},

	mounted() {
		this.fetch_picture();
	},

	methods: {
		async fetch_picture() {
		try {
			const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const route = useRoute();
			const username = route.query.username;
			const params = new URLSearchParams({ username: username });
			const response = await fetch(`/endpoint/user/profilepic/?${params.toString()}`, {
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
		async uploadProfilePic(event) {
      	
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
		},

		async changeProfilePicture () {
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
	}
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
</style>