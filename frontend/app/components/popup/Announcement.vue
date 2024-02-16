<!-- components/popup/Goal.vue -->

<template>
	<div class="popup">
	  <div class="popup-content">
		<!-- Your pop-up content goes here -->
		<p style="color: rgb(0, 255, 98); font-size: 200px;"> Goal!!!</p>
		<!-- <button type="button" class="btn btn-primary" @click="closePopup">Close</button> -->
	  </div>
	  <div>
    	<p v-if="countdown > 0">Countdown: {{ countdown }}</p>
    	<p v-else>Countdown finished!</p>
  	  </div>
	</div>
  </template>
  
  <script>
  export default {
	data() {
    return {
      countdown: 4,
      intervalId: null,
    };
  },
  created() {
    this.startCountdown();
  },
  destroyed() {
    this.stopCountdown();
  },
	methods: {
	  closePopup() {
		this.$emit('close');
	  },
	  startCountdown() {
		this.intervalId = setInterval(() => {
			if (this.countdown > 0) {
				this.countdown--;
			} else {
				this.stopCountdown();
			}
		}, 1000);
	  },
	  stopCountdown() {
		clearInterval(this.intervalId);
		setTimeout(() => {
			this.closePopup();
		}, 0);
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
	background: #ede8e800;
	padding: 200px;
	border-radius: 8px;
  }
  </style>
  