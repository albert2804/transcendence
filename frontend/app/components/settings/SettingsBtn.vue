<template>
      <div class="nes-container is-rounded clickable" style="background-color: #ff7c7c; position: relative; text-align: center;" type="button" data-bs-toggle="offcanvas" data-bs-target="#settingsCanvas" aria-controls="settingsCanvas">
        <i class="bi bi-gear" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
      </div>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="settingsCanvas" aria-labelledby="settingsCanvasLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="settingsCanvasLabel">Settings</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <RunningBanner />
          <div v-if="loginStatus === 1">
            
            <button type="button" class="nes-btn is-success clickable"  @click="openPopupName" style="width: 100%;">Change Alias</button>
            <button type="button" class="nes-btn is-success clickable" @click="openPopupPw" style="width: 100%;">Change Password</button>
            <button type="button" class="nes-btn is-success clickable" @click="openPopupPic" style="width: 100%;">Change Pictures</button>
            <button type="button" class="nes-btn is-success clickable" @click="openPopupMap" style="width: 100%;">Choose Map</button>
            
            <SettingsName :openPopup="PopupName" @close-popup="PopupName = false"/>
            <SettingsPic :openPopup="PopupPic" @close-popup="PopupPic = false"/>
            <SettingsPw :openPopup="PopupPw" @close-popup="PopupPw = false"/>
            <SettingsMap :openPopup="PopupMap" @close-popup="PopupMap = false"/>
          </div>
          <div v-if="! loginStatus">
            <p>Please log in to access settings</p>
            <button type="button" class="btn nes-btn btn-primary" data-bs-dismiss="offcanvas" @click="openLogin">Login</button>
          </div>
        </div>
      </div> 
  </template>

<script>
import { ref } from 'vue';
import { isLoggedIn } from '~/store';

const PopupName = ref({ value: false });;
const PopupPic = ref({ value: false });;
const PopupPw = ref({ value: false });;
const PopupMap = ref({ value: false });;

export default {
  name: 'SettingsBtn',
  data() {
    return {
      loginStatus: isLoggedIn
    }
  },
  watch: {
    isLoggedIn: {
      immediate: true,
      handler(newValue) {
        this.loginStatus = newValue;
      }
    }
  },
  setup() {
    return {
      PopupName,
      PopupPic,
      PopupPw,
      PopupMap,
    };
  },
  methods: {
    openLogin() {
      this.$router.push('/login');
    },

    openPopupName() {
      this.PopupName.value = true;
    },

    openPopupPic() {
      this.PopupPic.value = true;
    },

    openPopupPw() {
      this.PopupPw.value = true;
    },

    openPopupMap() {
      this.PopupMap.value = true;
    },
  }
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
