<template>

	<div class="container profilepic">
	  <div v-if="userProfilePic">
		<img :src=userProfilePic.url alt="Profile Picture" style="width: 200px; height: auto;">
	  </div>
	  <div v-else>
		<p>Loading failure for Profile Pic</p>
	  </div>
	</div>
  </template>

  <script>
  import { useRoute } from 'vue-router';

  export default{
	data(){
		return {
			userProfilePic: '{}',
		};
	},

	mounted() {
		this.fetch_picture();
	},

	methods: {
		async fetch_picture() {
		  try {
			const route = useRoute();
        	const username = route.query.username;
		    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const params = new URLSearchParams({ username: username });
			const response = await fetch(`/endpoint/user/profilepic?${params.toString()}`, {
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
		
	}
}
</script>

<style>
	/* img {
		image-rendering: pixelated;

	}
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
	} */
</style>