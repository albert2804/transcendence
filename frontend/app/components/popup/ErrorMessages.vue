<template>
	<div>
	  <div class="modal" :class="{ 'show': isVisible }" tabindex="-1" role="dialog" v-if="isVisible">
		<div class="modal-dialog">
		  <div class="modal-content">
			<div class="modal-header">
			  <h5 class="modal-title">{{ modalTitle }}</h5>
			  <button type="button" class="btn-close" @click="resetModal"></button>
			</div>
			<div class="modal-body">
			  {{ content }}
			</div>
		  </div>
		</div>
	  </div>
	</div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
	props: {
	  isVisible: Boolean,
	  content: String,
	  modalTitle: String,
	},
	methods: {
	  resetModal() {
		// Emit an event or handle the modal reset logic if needed
		this.$emit('hidden');
	  },
	},
  };
  </script>
  