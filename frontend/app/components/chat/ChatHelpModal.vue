<template>
  <div class="modal" id="helpmodal" tabindex="-1">
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
		<br>
		<p>- Left click on a user to open the chat</p>
		<p>- Click on a username in the chatbox header to view their profile</p>
		<br>
        <p style="margin-top: 10px; font-weight: bold;">Helpful chat commands:</p>
        <p><code>/play</code> - Invite/Accept user to play game</p>
        <p><code>/dont_play</code> - Reject game invitation</p>
        <p><code>/dont_play_tournament</code> - Reject tournament game invitation</p>
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
  name: 'ChatHelpModal',
  methods: {
  }
}
</script>

<style scoped>
.modal-body p {
  font-size: 0.8rem;
}
</style>