<!-- components/Popup.vue -->

<template>
	<div class="popup">
	  <div class="popup-content">
		<!-- Your pop-up content goes here -->
		<p>This is a pop-up!</p>
		<button type="button" class="btn btn-primary" @click="closePopup">Close</button>
	  </div>
	</div>
  </template>
  
  <script>
  export default {
	methods: {
	  closePopup() {
		this.$emit('close');
	  },
	},
  };
  </script>
  
  <style scoped>
  .popup {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
  }
  
  .popup-content {
	background: #fff;
	padding: 20px;
	border-radius: 8px;
  }
  </style>
  