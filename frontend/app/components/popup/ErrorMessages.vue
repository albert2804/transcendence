<template>
	<div v-if="openPopup" class="popup">
		<div class="content_container">
			<div v-if="error" class="error_container">
				<p style="text-align: center; color: white;">{{error}}</p>
				<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
			</div>
			<div v-if="message" class="message_container">
				<p style="text-align: center; color: white;">{{message}}</p>
				<button type="button" @click="closePopup" class="btn-close" aria-label="Close"></button>
			</div>
		</div>
	</div>
</template>

  <script>
export default {
  props: {
    openPopup: Boolean,
	error: String,
	message: String,
  },
  data(){
		return {
			content: '',
			label: '',
		};
	},

	methods: {
		closePopup() {
			this.$emit('close-popup');
		},
	},
}
</script>

<style>
  .card-size {
    min-width: px;
    max-width: 400px;
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
  background-color: #e45c10;
  top: 50%; /* Position it in the vertical center of the viewport */
  left: 50%; /* Position it in the horizontal center of the viewport */
  transform: translate(-50%, -50%); /* Center the popup exactly */
  padding: 20px; /* Padding around the content */
  border: 1px solid #ccc; /* Border */
  border-radius: 8px; /* Border radius */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle depth effect */
  width: 50vw;
  height: 10vw;
  white-space: normal;
  z-index: 1000;
}

.error_container {
	background-color: #f44336;
	position: fixed; /* Fixed positioning to overlay on top of other content */
	top: 50%; /* Position it in the vertical center of the viewport */
	left: 50%; /* Position it in the horizontal center of the viewport */
	transform: translate(-50%, -50%); /* Center the popup exactly */
	padding: 20px; /* Padding around the content */
	border: 1px solid #ccc; /* Border */
	border-radius: 8px; /* Border radius */
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle depth effect */
	width: 50vw;
	height: 10vw;
	white-space: normal;
	/* text-align: justify; */
	z-index: 1000;
}

.message_container {
	background-color: #4CAF50;
	position: fixed; /* Fixed positioning to overlay on top of other content */
	top: 50%; /* Position it in the vertical center of the viewport */
	left: 50%; /* Position it in the horizontal center of the viewport */
	transform: translate(-50%, -50%); /* Center the popup exactly */
	padding: 20px; /* Padding around the content */
	border: 1px solid #ccc; /* Border */
	border-radius: 8px; /* Border radius */
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle depth effect */
	width: 50vw;
	height: 10vw;
	white-space: normal;
	z-index: 1000;
}
</style>
