<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value
  })
</script>

<template>
  <div v-show="isLoggedIn === 1">
    <!-- v-if="connected" -->
    <div  class="nes-container is-rounded chatbutton" style="position: relative; text-align: center;" type="button" data-bs-toggle="offcanvas" data-bs-target="#chatCanvas" aria-controls="chatCanvas">
      <span class="badge rounded-pill bg-danger" v-if="messageAlert != 0" style="position: absolute; transform: translate(-150%, -140%);">
        {{ messageAlert }}
      </span>
    <i class="bi bi-chat-right-fill" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -50%);"></i>
    </div>
  </div>
  <!--  CHAT HELP MODAL -->
	<div class="modal" tabindex="-1" id="helpmodal">
		<div class="modal-dialog">
			<div class="modal-content nes-container">
			<div class="modal-header">
				<h5 class="modal-title">Chat Help</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			</div>
			<div class="modal-body">
				<p><i class="bi bi-star-fill" style="color: #007bff; font-size: 1.2rem;"></i> - You are friends</p>
				<p><i class="bi bi-x-circle" style="color: red; font-size: 1.2rem;"></i> - You blocked this user</p>
				<p><i class="bi bi-x-circle-fill" style="color: red; font-size: 1.2rem;"></i> - This user blocked you</p>
				<p style="margin-top: 10px; font-weight: bold;">Helpful chat commands:</p>
        <p><code>/play</code> - Invite/Accept user to play game</p>
        <p><code>/dont_play</code> - Reject game invitation</p>
				<p><code>/block</code> - Block user</p>
				<p><code>/unblock</code> - Unblock user</p>
				<p><code>/friend</code> - Invite/Accept friend request</p>
				<p><code>/unfriend</code> - Unfriend user</p>
			</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'ChatButton',
  data() {
    return {
      loading: true,
      connected: false,
      messageAlert: 0,
    }
  },
  expose: ['handleMessageAlert', 'setToConnected', 'setToDisconnected'],
  methods: {
	closeHelpModal() {
		this.$nextTick(() => {
			var mood = document.getElementById('helpmodal');
			var bsModal = bootstrap.Modal.getInstance(mood);
			bsModal.hide();
		});
	},
    handleMessageAlert(value) {
      this.messageAlert = value;
    },
    toggleChatBox() {
      // if (this.connected === true) {
        this.$nextTick(() => {
          var mood = document.getElementById('chatCanvas');
          var bsOffcanvas = bootstrap.Offcanvas.getInstance(mood);
          bsOffcanvas.toggle();
        });
      // }
    },
    setToConnected() {
      this.connected = true;
      this.loading = false;
    },
    setToDisconnected() {
      this.connected = false;
      this.showChatBox = false;
    }
  }
}
</script>

<style>

.chatbutton {
  width: 55px;
  height: 40px;
}
</style>