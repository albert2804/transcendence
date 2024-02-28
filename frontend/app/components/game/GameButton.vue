<template>
  <div v-if="state === 'connected'" class="nes-container is-rounded clickable" style="background-color: #99e857; position: relative; text-align: center;" @click="showGameModal">
    <i class="bi bi-controller" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
  </div>
  <div v-if="state === 'loading'" class="nes-container is-rounded" style="background-color: #99e857; position: relative; text-align: center;">
	<i class="bi bi-hourglass" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
  </div>
  </template>

<script>
import { gameButtonState } from '~/store';
export default {
  name: 'GameButton',
  data() {
    return {
      state: gameButtonState,
    }
  },
  watch: {
    state: {
      immediate: true,
      handler(newValue) {
		this.state = newValue;
      }
    }
  },
  methods: {
    showGameModal() {
      this.$nextTick(() => {
        var bsModal = bootstrap.Modal.getInstance(document.getElementById('pongmodal'));
        if (!bsModal) {
          bsModal = new bootstrap.Modal(document.getElementById('pongmodal'));
        }
        bsModal.show();
      });
    },
  },
}
</script>