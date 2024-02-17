<script setup>
  // Listen to changes of the isLoggedIn from store/index.js
  import { isLoggedIn } from '~/store';
  watchEffect(() => {
  isLoggedIn.value = isLoggedIn.value
})
</script>

<template>
  <div v-if="isLoggedIn === 1">
    <button class="settings" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">⚙</button>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel">Settings</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
          <button type="button" class="btn btn-primary"  @click="openPopupName">Change Username</button>
          <button type="button" class="btn btn-primary" @click="openPopupPw">Change Password</button>
          <button type="button" class="btn btn-primary" @click="openPopupPic">Change Profile Picture</button>
      
          <SettingsName :openPopup="PopupName" @close-popup="PopupName = false"/>
          <SettingsPic :openPopup="PopupPic" @close-popup="PopupPic = false"/>
          <SettingsPw :openPopup="PopupPw" @close-popup="PopupPw = false"/>
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
  }
};
</script>

<style>
.settings {
  border: none;
  background: none;
  position: fixed; 
  top: 5px; 
  right: 20px; 
  z-index: 2; 
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
}

.offcanvas-body {
  display: flex;
  flex-direction: column; 
}

.btn-primary {
  margin-bottom: 10px;
}

</style>
