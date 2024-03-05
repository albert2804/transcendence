<!-- 
In Nuxt3 this 'default' layout is used by default for all pages.
If you want to use a different layout for a page, you can create a new one in this layouts/ folder and then use it in the page.
To use it you have to add a script tag at the top of the page and define the layout there.
Example:

<script setup>
  definePageMeta({
    layout: 'otherlayout',
  })  
</script>
-->

<template>
  <div class="justify-content-center">
    <ChatHelpModal />
    <div class="nes-container is-rounded with-title vh-80 is-centered">
      <div class="buttonlist">
        <SettingsBtn />
        <ChatButton />
        <GameButton />
      </div>
      <div class="d-flex justify-content-center vh-80">
        <NuxtPage :page-key="pageKey.toString()" />
      </div>
      <div>
        <NavBar />
      </div>
    </div>
  </div>
</template>

<script>
  import { isLoggedIn, userName, userId } from '~/store';
  export default {
    setup() {
      const pageKey = ref(Date.now())

      onMounted(async () => {
        // initate the csrf token!
        // this calls django to create a csrf token as cookie
        // this token is needed for POST requests to django
        try {
          const response = await fetch('/endpoint/api/csrf')
        } catch (error) {
          console.error('Error:', error)
        }
        // check if user is logged in and set isLoggedIn in store/index.js
        // so other components can use or listen to it
        try {
          const response = await fetch('/endpoint/api/auth_status', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const data = await response.json();
          if (data.authenticated) {
            isLoggedIn.value = 1
            userName.value = data.username
            userId.value = data.user_id
          } else {
            isLoggedIn.value = 0
          }
        } catch (error) {
          console.error('Error:', error);
          isLoggedIn.value = 0
        }
      })

      // Following is to force rerendering of the pages
      onBeforeUpdate(() => {
        pageKey.value = Date.now()
      })
      return { pageKey }
    },
  }
</script>

<style>
.justify-content-center {
  justify-content: center;
}

.nes-container.is-rounded.with-title.vh-80.is-centered {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 95vh;
  margin: 20px 30px 30px;
}

@media screen and (max-width: 800px) {
  .nes-container.is-rounded.with-title.vh-80.is-centered {
    margin: 10px 5px 5px;
    padding-left: 0px;
    padding-right: 0px;
  }
}

.d-flex.justify-content-center.vh-80 {
  overflow: auto;
}

.buttonlist {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-right: 15px;
  z-index: 3;
  right: 0;
}
</style>