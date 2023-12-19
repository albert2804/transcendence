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
  <div>
    <NavBar />
    <ChatButton />
    <slot />
  </div>
</template>
