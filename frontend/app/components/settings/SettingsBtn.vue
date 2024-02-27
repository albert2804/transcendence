<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
    <div class="nes-container is-rounded" style="background-color: #ff7c7c; position: relative; text-align: center;" type="button" data-bs-toggle="offcanvas" data-bs-target="#settingsCanvas" aria-controls="settingsCanvas">
      <i class="bi bi-gear" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="settingsCanvas" aria-labelledby="settingsCanvasLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="settingsCanvasLabel">Settings</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <!-- ALERTS -->
        <div v-if="recvmessage" class="alert alert-success" style="min-width: 14em" role="alert">{{ recvmessage }}</div>
        <div v-if="recverror" class="alert alert-danger" style="min-width: 14em" role="alert">{{ recverror }}</div>
        <div v-if="isLoggedIn === 1">
          <button type="button" class="nes-btn is-success"  @click="openPopupName">Change Nickname</button>
          <button type="button" class="nes-btn is-success" @click="openPopupPw">Change Password</button>
          <button type="button" class="nes-btn is-success" @click="openPopupPic">Change Pictures</button>
      
          <SettingsName :openPopup="PopupName" @close-popup="PopupName = false" @message-from-child="handleUpdate" />
          <SettingsPic :openPopup="PopupPic" @close-popup="PopupPic = false" @message-from-child="handleUpdate" />
          <SettingsPw :openPopup="PopupPw" @close-popup="PopupPw = false"/>
        </div>
        <div v-if="! isLoggedIn">
          <p>Please log in to access settings</p>
		  <button type="button" class="btn nes-btn btn-primary" data-bs-dismiss="offcanvas" @click="openLogin">Login</button>
        </div>
      </div>
    </div> 
  </template>

<script>
import { ref } from 'vue';

const PopupName = ref(false);
const PopupPic = ref(false);
const PopupPw = ref(false);
let recvmessage = ref('');
let recverror = ref('');

const openPopupName = () => {
  PopupName.value = true;
  this.$nextTick(() => {
    this.$refs.popupInput.focus();
  });
};
const openPopupPic = () => {
  PopupPic.value = true;
};
const openPopupPw = () => {
  PopupPw.value = true;
};

export default {
  setup() {
    return {
      PopupName,
      PopupPic,
      PopupPw,
      handleUpdate,
      handleError,
      message: '',
      error: '',
    };
  },
 
  methods: {
    openLogin() {
      this.$router.push('/login');
    },
    handleUpdate(message, error) {
      recverror = error;
      recvmessage = message;
      console.log('print from parent', recverror);
      this.$forceUpdate();
    },
    resetMessages() {
      recverror = '';
      recvmessage = '';
      this.$forceUpdate();
    }
  },
};
</script>

<style>

.offcanvas-body {
  display: flex;
  flex-direction: column; 
}

.btn-primary {
  margin-bottom: 10px;
}

</style>
