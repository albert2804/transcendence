<template>
  <div class="page-container">
    <h1 class="title">Welcome to FT_TRANSCENDENCE</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.page-container {
  margin: auto;
  overflow: hidden;
  align-self: center;
  background-image: url('/background_home_big.png');
  background-size: cover;
  height: 150%;
  width: 100%;
  display: flex;
}

.title {
  font-size: 4vw;
  color: black;
  overflow: hidden;
  z-index: 2;
  text-shadow: 4px 4px 0px white, 
               4px -4px 0px white, 
               -4px 4px 0px white, 
               -4px -4px 0px white, 
               4px 0px 0px white, 
               0px 4px 0px white, 
               -4px 0px 0px white, 
               0px -4px 0px white;
  padding-top: 25vh;
  border-radius: 10px;
}

html, body {
    height: 100%;
    margin: 0;
    overflow: hidden;
  }

</style>
