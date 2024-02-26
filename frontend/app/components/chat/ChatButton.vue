<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value
  })
</script>

<template>
  <ChatBox @closeChat="toggleChatBox" @connected="setToConnected" @disconnected="setToDisconnected" @loading="loading = true" @unreadMessages="handleMessageAlert"/>
  <div v-show="isLoggedIn === 1">
    <div v-if="connected && !loading" class="nes-container is-rounded clickable" style="background-color: #ffea76; position: relative; text-align: center;" type="button" data-bs-toggle="offcanvas" data-bs-target="#chatCanvas" aria-controls="chatCanvas">
      <span class="badge rounded-pill bg-danger" v-if="messageAlert != 0" style="position: absolute; transform: translate(-150%, -140%);">
        {{ messageAlert }}
      </span>
      <i class="bi bi-chat" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -60%);"></i>
    </div>
    <div v-if="loading" class="nes-container is-rounded" style="background-color: #ffea76; position: relative; text-align: center;">
      <i class="bi bi-hourglass" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
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
  methods: {
    handleMessageAlert(value) {
      this.messageAlert = value;
    },
    toggleChatBox() {
      if (this.connected === true) {
        this.$nextTick(() => {
          var mood = document.getElementById('chatCanvas');
          var bsOffcanvas = bootstrap.Offcanvas.getInstance(mood);
          bsOffcanvas.toggle();
        });
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
