<template>
  <div
    ref="modalRef"
    @keydown.esc="closeModal"
    class="modal fade"
    :id="modalId" tabindex="-1"
    :aria-labelledby="ariaLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    style="max-height: 100vh;">
    <div class="modal-dialog fullscreen-modal align-items-center">
      <div class="modal-content">
        <div class="modal-body">
          <GameField ref="ponggamefieldRef" @openModal="openModal" @close-modal="closeModal"/>
        </div>
      </div>
    </div>
    <button @click="closeModal" type="button" class="btn-close" aria-label="Close" style="position: absolute; top: 10px; right: 10px;"></button>
  </div>
</template>

<script>
export default {
  name: 'GameModal',
  setup() {
    const modalRef = ref(null);
    const { toggle } = useFullscreen(modalRef);
    // function to open fullscreen
    function openFullscreen() {
      if (document.fullscreenElement !== modalRef.value) {
        toggle();
      }
    }
    // function to close fullscreen
    function closeFullscreen() {
      if (document.fullscreenElement === modalRef.value) {
        toggle();
      }
    }

    return {
      openFullscreen,
      closeFullscreen,
      modalRef,
    }
  },
  props: {
    modalId: String,
    ariaLabel: String,
  },
  mounted() {
    // listen to modal events to open and close fullscreen
    var mood = document.getElementById(this.modalId);
    // mood.addEventListener('shown.bs.modal', this.openFullscreen);
    // mood.addEventListener('hidden.bs.modal', this.closeFullscreen);
  },
  methods: {
    openModal() {
      var mood = document.getElementById(this.modalId);
      // check if the modal is already shown
      if (mood.classList.contains('show')) {
        return;
      }
      var bsModal = new bootstrap.Modal(mood);
      bsModal.show();
    },
    closeModal() {
      this.closeFullscreen(); // smoother than closing fullscreen after modal is hidden
      if (this.$refs.ponggamefieldRef) {
        this.$refs.ponggamefieldRef.giveUpGame();
      }
      setTimeout(() => {
        var mood = document.getElementById(this.modalId);
        var bsModal = bootstrap.Modal.getInstance(mood);
        bsModal.hide();
      }, 0);
    },
  },
};
</script>

<style>
  .btn-close {
    background-color: white;
  }
  .modal-dialog.fullscreen-modal {
    max-width: 100%;
    margin: 0;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    height: 100vh;
    display: flex;
    overflow: hidden;
  }
</style>
