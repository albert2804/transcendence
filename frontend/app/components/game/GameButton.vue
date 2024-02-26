<template>
  <div class="nes-container is-rounded clickable" style="background-color: #99e857; position: relative; text-align: center;" @click="showGameModal">
    <i class="bi bi-controller" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
  </div>
  </template>

<script>
export default {
  name: 'GameButton',
  // setup() {
  //   const fullscreen = ref(false);
  //   const { toggle } = useFullscreen();

  //   function openFullscreen() {
  //     // console.log('openFullscreen');
  //     fullscreen.value = !fullscreen.value;
  //     toggle();
  //   }

  //   return {
  //     fullscreen,
  //     openFullscreen,
  //   }
  // },
  methods: {
    showGameModal() {
      this.$nextTick(() => {
          new bootstrap.Modal(document.getElementById('pongmodal')).show();
      });
      // useFullscreen
      // this.openFullscreen();
    },
  },
}
</script>