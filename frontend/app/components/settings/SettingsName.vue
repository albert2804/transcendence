<template>
	<div v-if="openPopup" class="popup">
		<div class="username_container nes-field">
			<label for="username">Change Alias</label>
			<input class="nes-input" type="text" id="username" name="username" v-model="editedName" @keydown.enter="saveChanges" @blur="cancelChanges">
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
					if (this.$route.path === '/userinfopage') {
						reloadNuxtApp({ path: '/userinfopage' });
					}
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
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
</style>
