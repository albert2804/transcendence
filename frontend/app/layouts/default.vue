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
  <!-- <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet"> -->
  <!-- minify -->
  <!-- <link href="https://unpkg.com/nes.css@2.3.0/css/nes.min.css" rel="stylesheet" /> -->
  <!-- core style only -->
  <!-- <link href="https://unpkg.com/nes.css/css/nes-core.min.css" rel="stylesheet" /> -->
  <div class="nes-container  is-rounded with-title vh-80 is-centered" style="display: flex; height: calc(100vh - 20px); justify-content: center; align-items: center; min-width: 600px">
    <!-- <div style="display: flex; justify-content: center; margin-top: 20vh;"> -->
    <!-- <p class="title">A 42 PONG GAME</p> -->
    <SettingsBtn />
    <slot />
    <ChatButton />
    
    <NavBar />
  </div>
</template>

<script>
  import { isLoggedIn } from '~/store';
  export default {
    setup() {
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
          } else {
            isLoggedIn.value = 0
          }
        } catch (error) {
          console.error('Error:', error);
          isLoggedIn.value = 0
        }
      })
    },
  }
</script>
