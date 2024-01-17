<template>
  <div class="modal fade"
    :id="modalId" tabindex="-1"
    :aria-labelledby="ariaLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    @keydown.esc="closeModal"
    @keydown="handleKeyDown"
    @keyup="handleKeyUp">
    <div class="modal-dialog fullscreen-modal align-items-center">
      <div class="modal-content">
        <div class="modal-body">
          <GameField ref="ponggamefieldRef"/>
        </div>
      </div>
    </div>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" style="position: absolute; top: 10px; right: 10px;"></button>
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
  methods: {
    closeModal() {
      // console.log('close modal');
      setTimeout(() => {
        var mood = document.getElementById(this.modalId);
        var bsModal = bootstrap.Modal.getInstance(mood);
        bsModal.hide();
      // }, 1000);
      }, 0);
    },
    handleKeyDown(event) {
      if (this.$refs.ponggamefieldRef) {
        this.$refs.ponggamefieldRef.handleKeyDown(event);
      }
    },
    handleKeyUp(event) {
      if (this.$refs.ponggamefieldRef) {
        this.$refs.ponggamefieldRef.handleKeyUp(event);
      }
    }
  },
};
</script>

<style>
  .modal-dialog.fullscreen-modal {
    max-width: 100%;
    margin: 0;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    height: 100vh;
    display: flex;
  }
</style>
