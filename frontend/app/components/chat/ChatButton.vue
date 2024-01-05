<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
    isLoggedIn.value = isLoggedIn.value
  })
</script>

<template>
  <div v-show="isLoggedIn === 1">
    <ChatBox v-show="showChatBox" class="chat-box" @closeChat="toggleChatBox" @connected="setToConnected" @disconnected="setToDisconnected" @loading="loading = true" />
    <button v-show="!showChatBox" class="btn btn-primary round-button" @click="toggleChatBox">
      <div v-if="connected">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-chat" viewBox="0 0 16 16">
          <path d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894m-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.637l.003-.01c.248-.72.45-1.548.524-2.319C.743 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.52.263-1.639.742-3.468 1.105z"/>
        </svg>
      </div>
      <div v-else-if="loading" class="spinner-container">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </button>
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
    }
  },
  methods: {
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
  position: absolute;
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
  position: absolute;
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