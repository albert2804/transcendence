<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

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
        <div v-if="isLoggedIn === 1">
          <button type="button" class="nes-btn is-success clickable"  @click="openPopupName" style="width: 100%;">Change Alias</button>
          <button type="button" class="nes-btn is-success clickable" @click="openPopupPw" style="width: 100%;">Change Password</button>
          <button type="button" class="nes-btn is-success clickable" @click="openPopupPic" style="width: 100%;">Change Pictures</button>
      
          <SettingsName :openPopup="PopupName" @close-popup="PopupName = false"/>
          <SettingsPic :openPopup="PopupPic" @close-popup="PopupPic = false"/>
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

const openPopupName = () => {
  PopupName.value = true;
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
    };
  },
  methods: {
	openLogin() {
	  this.$router.push('/login');
	}
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
