<template>
  <div class="modal fade" :id="modalId" tabindex="-1" :aria-labelledby="ariaLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <!-- <h5 class="modal-title">{{ modalTitle }}</h5> -->
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          <!-- <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button> -->
        </div>
        <div class="modal-body">
          <!-- <GameField :paddleSize="20" @game-end="closeModal" /> -->
          <GameField />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameModal',
  props: {
    modalTitle: String,
    modalId: String,
    ariaLabel: String,
  },
  // listener useful to trigger the closeModal method when the modal is closed by clicking on the close button
  // also possible to use the @click event on the close button and remove this listener
  // but for now I leave it here because maybe it will be useful in the future
  mounted() {
    console.log('set listener for game modal');
    document.getElementById(this.modalId).addEventListener('hidden.bs.modal', this.closeModal);
  },
  beforeDestroy() {
    console.log('remove listener for game modal');
    document.getElementById(this.modalId).removeEventListener('hidden.bs.modal', this.closeModal);
  },
  methods: {

    // this method is here to get emitted from GameField.vue when the game ends ?!?
    // or maybe it is not needed at all
    // we will see
    closeModal() {
      console.log('close modal');
      setTimeout(() => {
        var mood = document.getElementById(this.modalId);
        var bsModal = bootstrap.Modal.getInstance(mood);
        bsModal.hide();
      }, 1000);
    },
  },
};
</script>
