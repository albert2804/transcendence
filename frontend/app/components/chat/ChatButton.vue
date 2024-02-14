<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value
  })
</script>

<template>
  <div v-show="isLoggedIn === 1">
    <ChatBox v-show="showChatBox" class="chat-box" @closeChat="toggleChatBox" @connected="setToConnected" @disconnected="setToDisconnected" @loading="loading = true" @unreadMessages="handleMessageAlert"/>
    <button v-if="connected && !showChatBox" class="btn btn-primary round-button" @click="toggleChatBox">
      <div style="position: relative; text-align: center;">
      <span class="badge rounded-pill bg-danger" v-if="messageAlert != 0" style="position: absolute; transform: translate(-150%, -140%);">
        {{ messageAlert }}
      </span>
		<div class="bi bi-chat" style="font-size: 2.0rem; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"></div>
      </div>
    </button>
    <button v-else-if="loading && !showChatBox"  class="btn btn-primary round-button" @click="toggleChatBox">
      <div class="spinner-container">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </button>
  </div>
  <!--  CHAT HELP MODAL -->
	<div class="modal" tabindex="-1" id="helpmodal">
		<div class="modal-dialog">
			<div class="modal-content">
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
      showChatBox: false,
      loading: true,
      connected: false,
      messageAlert: 0,
    }
  },
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
      if (this.connected === true) {
        this.showChatBox = !this.showChatBox;
      }
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
.round-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 2;
}

.spinner-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-box {
  position: fixed;
  bottom: 10px;
  right: 20px;
  z-index: 2;
}

@media (max-width: 600px) {
  .chat-box {
    bottom: 10;
    right: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-end;
  }
}
</style>