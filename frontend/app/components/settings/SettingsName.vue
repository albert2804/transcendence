<template>
	<div v-if="openPopup" class="popup">
		<div class="username_container">
			<label for="username">Change Alias:</label>
			<input type="text" id="username" name="username" v-model="editedName" @keydown.enter="saveChanges" @blur="cancelChanges">
			<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
		</div>
	</div>
  </template>

  <script>
export default {
  props: {
    openPopup: Boolean,
  },
  data(){
		return {
			editedName: '',
			originalName: '',
			nameResponse: null,
		};
	},

	methods: {
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
				const data = await response.json()
				this.error = data.error;
				this.message = data.status;
				this.closePopup();
				this.sendMessagetoParent(this.message, this.error);
				if (response.status === 200){
					await this.$router.push('/userinfopage');
					location.reload();
				}
			} catch (error) {
				console.error('Error updating user alias:', error);
			}
		},
		
		cancelChanges() {
			this.editedName = this.originalName;
			this.$emit('close-popup');
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

.popup {
  position: fixed; /* Fixed positioning to overlay on top of other content */
  top: 50%; /* Position it in the vertical center of the viewport */
  left: 50%; /* Position it in the horizontal center of the viewport */
  transform: translate(-50%, -50%); /* Center the popup exactly */
  background-color: white; /* Background color */
  padding: 20px; /* Padding around the content */
  border: 1px solid #ccc; /* Border */
  border-radius: 8px; /* Border radius */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle depth effect */
}
</style>
