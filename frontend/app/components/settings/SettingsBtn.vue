<template>
  <div>
    <div class="nes-container is-rounded clickable" style="background-color: #ff7c7c; position: relative; text-align: center;" type="button" data-bs-toggle="offcanvas" data-bs-target="#settingsCanvas" aria-controls="settingsCanvas">
      <i class="bi bi-gear" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="settingsCanvas" aria-labelledby="settingsCanvasLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="settingsCanvasLabel">Settings</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="settingsCanvas" aria-labelledby="settingsCanvasLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="settingsCanvasLabel">Settings</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div v-if="recvmessage" class="alert alert-success" style="min-width: 14em" timeout="30s" role="alert">{{ recvmessage }}</div>
          <div v-if="recverror" class="alert alert-danger" style="min-width: 14em" role="alert">{{ recverror }}</div>
          <div v-if="loginStatus === 1">
                <button type="button" class="nes-btn is-success clickable"  @click="openPopupName" style="width: 100%;">Change Alias</button>
                <button type="button" class="nes-btn is-success clickable" @click="openPopupPw" style="width: 100%;">Change Password</button>
                <button type="button" class="nes-btn is-success clickable" @click="openPopupPic" style="width: 100%;">Change Picture</button>
                <button type="button" class="nes-btn is-success clickable" @click="openPopupMap" style="width: 100%;">Choose Map</button>
                <button type="button" class="nes-btn is-success clickable" @click="openPopup2FA">Enable 2FA authentication</button>
                
                <SettingsName :openPopup="PopupName" @close-popup="PopupName = false" @message-from-child="handleUpdate" />
                <SettingsPic :openPopup="PopupPic" @close-popup="PopupPic = false" @message-from-child="handleUpdate" />
                <SettingsPw :openPopup="PopupPw" @close-popup="PopupPw = false" @message-from-child="handleUpdate" />
                <SettingsMap :openPopup="PopupMap" @close-popup="PopupMap = false"/>
                {{ username }}
                <SettingsDo2FA :openPopup="Popup2FA" :username="username" @close-popup="Popup2FA = false"/>
          </div>
          <div v-if="!loginStatus">
              <p>Please log in to access settings</p>
              <button type="button" class="btn nes-btn btn-primary" data-bs-dismiss="offcanvas" @click="openLogin">Login</button>
          </div>
        </div>
        <div v-if="loginStatus != 1">
          <p>Please log in to access settings</p>
          <button type="button" class="btn nes-btn btn-primary" data-bs-dismiss="offcanvas" @click="openLogin">Login</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { ref, watchEffect, watch } from 'vue';
import { isLoggedIn, userName } from '~/store';

export default {
  name: 'SettingsBtn',
  data() {
    return {
      loginStatus: isLoggedIn,
      recvmessage:'',
      recverror:'',
    }
  },
  setup() {
    const handleUpdate = ref(false);
    const handleError = ref(false);
    const message = ref('');
    const error = ref('');
    const PopupName = ref(false);
    const PopupPic = ref(false);
    const PopupPw = ref(false);
    let recvmessage = ref('');
    let recverror = ref('');
    const PopupMap = ref(false);
    const loginStatus = ref(isLoggedIn.value);
    const Popup2FA = ref(false);
    const username = ref(userName.value);

    watch(userName, (newVal) => {
      username.value = newVal;
    });

    console.log('SETUP: username', username.value);

    const openPopupName = () => {
      PopupName.value = true;
    };
    const openPopupPic = () => {
      PopupPic.value = true;
    };
    const openPopupPw = () => {
      PopupPw.value = true;
    };
    const openPopupMap = () => {
      PopupMap.value = true;
    };
    const openPopup2FA = () => {
      Popup2FA.value = true;
      console.log('openPopup2FA', Popup2FA.value);
};

    watchEffect(() => {
        loginStatus.value = isLoggedIn.value;
      });

    return {
      handleUpdate,
      error,
      message,
      loginStatus,
      PopupName,
      PopupPic,
      PopupPw,
      PopupMap,
      Popup2FA,
      openPopupName,
      openPopupPic,
      openPopupPw,
      openPopupMap,
      openPopup2FA,
      username,
    };
  },
 
  methods: {
    openLogin() {
      this.$router.push('/login');
    },
    async handleUpdate(message, error) {
      this.recverror = error;
      this.recvmessage = message;
      console.log('print from parent', this.recverror);
      this.$forceUpdate();
      this.resetMessages();
    },
    async resetMessages() {
      await new Promise(resolve => setTimeout(resolve, 3000));
      this.recverror = '';
      this.recvmessage = '';
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

.nes-btn {
  margin-bottom: 10px;
  width: 95%;
}

</style>
