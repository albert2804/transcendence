<template>
	<div class="profilepic">
	  <div v-if="userProfilePic">
		<img :src=userProfilePic.url alt="Profile Picture">
	  </div>
	  <div v-else>
		<p>Loading failure for Profile Pic</p>
	  </div>
	
	  <div>
    	<button type="button" class="btn btn-primary" @click="uploadpic">
      	<slot>Change Profile Picture</slot>
     	</button>
  	  </div>
	</div>
  </template>

  <script>
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
			const response = await fetch('/endpoint/user/profilepic', {
        		method: 'GET',
          		headers: {
            	'Content-Type': 'application/json',
            	'X-CSRFToken': csrfToken,
          	    }
       		 })
			this.userProfilePic = await response.json();
			} catch (error) {
				console.error('Error fetching user data:', error);
			}
		},
	},
};
</script>
