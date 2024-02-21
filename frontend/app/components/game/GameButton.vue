<template>
  <div class="nes-container is-rounded" style="background-color: #99e857; position: relative; text-align: center;" @click="showGameModal">
    <i class="bi bi-controller" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
  </div>
  </template>

<script>
export default {
  name: 'GameButton',
  methods: {
    showGameModal() {
      this.$nextTick(() => {
          new bootstrap.Modal(document.getElementById('pongmodal')).show();
      });
    },
  },
}
</script>