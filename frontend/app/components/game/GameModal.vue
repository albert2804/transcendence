<!-- :id="modalId" tabindex="-1"
:aria-labelledby="ariaLabel" -->
<template>
  <div
    :id="modalId" tabindex="-1"
    ref="modalRef"
    class="modal fade"
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
	  <div class="row">
      <!-- fullscreen button -->
      <button v-if="!fullscreen" @click="openFullscreen" type="button" class="btn" aria-label="Fullscreen" style="position: absolute; top: 20px; right: 80px; background-color: rgba(255, 255, 255, 0.494); width: 50px; height: 50px;">
        <i class="bi bi-arrows-fullscreen" style="color: black; font-size: 1.5rem;"></i>
      </button>
      <!-- exit fullscreen button -->
      <button v-if="fullscreen" @click="closeFullscreen" type="button" class="btn" aria-label="Exit Fullscreen" style="position: absolute; top: 20px; right: 80px; background-color: rgba(255, 255, 255, 0.494); width: 50px; height: 50px;">
        <i class="bi bi-fullscreen-exit" style="color: black; font-size: 1.5rem;"></i>
      </button>
      <!-- close modal button -->
      <button @click="closeModal" type="button" class="btn" aria-label="Close" style="position: absolute; top: 20px; right: 20px; background-color: rgba(255, 255, 255, 0.494); width: 50px; height: 50px;">
        <i class="bi bi-x-lg" style="color: black; font-size: 1.5rem;"></i>
      </button>
	  </div>
  </div>
</template>

<script>
export default {
  name: 'GameModal',
// 
// TODO: make ID useless (use ref instead)
// (need to change the showGameModal from GameButton)
// 
  props: {
    modalId: {
      type: String,
      default: 'pongmodal',
    }
  },
// 
// 
// 
  setup() {
    const modalRef = ref(null);
    const ponggamefieldRef = ref(null);
    const { toggle } = useFullscreen(modalRef);
    const fullscreen = ref(false);

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

    // function for the fullscreenchange event (to update the fullscreen variable for the button)
    function updateFullscreen() {
      fullscreen.value = document.fullscreenElement === modalRef.value;
    }

    // function to close the modal
    function closeModal() {
      closeFullscreen(); // smoother than closing fullscreen after modal is hidden
      if (ponggamefieldRef.value) {
        ponggamefieldRef.value.giveUpGame();
      }
      setTimeout(() => {
        var bsModal = bootstrap.Modal.getInstance(modalRef.value);
        bsModal.hide();
      }, 0);
      // setTimeout(() => {
      //   var mood = document.getElementById(modalId.value);
      //   var bsModal = bootstrap.Modal.getInstance(mood);
      //   bsModal.hide();
      // }, 0);
    }

    function handleKeyPress(event) {
      if (event.key === 'Escape') {
        closeModal();
        return;
      }
      ponggamefieldRef.value.handleKeyPress(event);
    }

    function handleKeyRelease(event) {
      ponggamefieldRef.value.handleKeyRelease(event);
    }

    onMounted(() => {
      document.addEventListener('fullscreenchange', updateFullscreen);
      // 
      window.addEventListener('keydown', handleKeyPress);
      window.addEventListener('keyup', handleKeyRelease);
    });

    onUnmounted(() => {
      document.removeEventListener('fullscreenchange', updateFullscreen);
      // 
      window.removeEventListener('keydown', handleKeyPress);
      window.removeEventListener('keyup', handleKeyRelease);
    });

    return {
      openFullscreen,
      closeFullscreen,
      modalRef,
      ponggamefieldRef,
      fullscreen,
      closeModal,
      handleKeyPress,
      handleKeyRelease,
    }
  },
  // props: {
  //   modalId: String,
  //   // ariaLabel: String,
  // },
  methods: {
    // openModal() {
    //   var mood = document.getElementById(this.modalId);
    //   // check if the modal is already shown
    //   if (mood.classList.contains('show')) {
    //     return;
    //   }
    //   var bsModal = new bootstrap.Modal(mood);
    //   bsModal.show();
    // },
    // openModal with ref instead of id
    openModal() {
      this.$nextTick(() => {
        var bsModal = bootstrap.Modal.getInstance(this.$refs.modalRef);
        bsModal.show();
      });
    },


    
    // closeModal() {
    //   this.closeFullscreen(); // smoother than closing fullscreen after modal is hidden
    //   if (this.$refs.ponggamefieldRef) {
    //     this.$refs.ponggamefieldRef.giveUpGame();
    //   }
    //   setTimeout(() => {
    //     var mood = document.getElementById(this.modalId);
    //     var bsModal = bootstrap.Modal.getInstance(mood);
    //     bsModal.hide();
    //   }, 0);
    // },
	// handleKeyPress(event) {
    // if (event.key === 'Escape') {
    //   this.closeModal();
    //   return;
    // }
	//   this.$refs.ponggamefieldRef.handleKeyPress(event);
	// },
	// handleKeyRelease(event) {
	//   this.$refs.ponggamefieldRef.handleKeyRelease(event);
	// }
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
