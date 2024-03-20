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
          <GameField ref="ponggamefieldRef" @openModal="openModal" @closeModal="closeModal" />
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
  props: {
	modalId: {
	  type: String,
	  required: true,
	},
  },
  setup() {
    const modalRef = ref(null);
    const ponggamefieldRef = ref(null);
    const fullscreen = ref(false);

    // function to open fullscreen
    function openFullscreen() {
      if (modalRef.value.requestFullscreen) {
        modalRef.value.requestFullscreen();
      } else if (modalRef.value.mozRequestFullScreen) {
        // Firefox
        modalRef.value.mozRequestFullScreen();
      } else if (modalRef.value.webkitRequestFullscreen) {
        // Chrome, Safari and Opera
        modalRef.value.webkitRequestFullscreen();
      } else if (modalRef.value.msRequestFullscreen) {
        // IE/Edge
        modalRef.value.msRequestFullscreen();
      }
    }
    // function to close fullscreen
    function closeFullscreen() {
      if (document.fullscreenElement) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
          // Firefox
          document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
          // Chrome, Safari and Opera
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
          // IE/Edge
          document.msExitFullscreen();
        }
      }
    }
    // function for the fullscreenchange event (to update the fullscreen variable for the button)
    function updateFullscreen() {
      fullscreen.value = document.fullscreenElement === modalRef.value;
    }
    // function to open the modal
    function openModal() {
      nextTick(() => {
        var bsModal = bootstrap.Modal.getInstance(modalRef.value);
        if (!bsModal) {
          bsModal = new bootstrap.Modal(modalRef.value);
        }
        bsModal.show();
      });
    }
    // function to close the modal
    function closeModal() {
      closeFullscreen(); // smoother than closing fullscreen after modal is hidden
      if (ponggamefieldRef.value) {
        ponggamefieldRef.value.giveUpGame();
      }
      setTimeout(() => {
        var bsModal = bootstrap.Modal.getInstance(modalRef.value)
		if (bsModal) {
		  bsModal.hide();
		}
      }, 0);
    }
    // function to handle keypress events
    function handleKeyPress(event) {
      if (event.key === 'Escape') {
        closeModal();
        return;
      }
      ponggamefieldRef.value.handleKeyPress(event);
    }
    // function to handle keyrelease events
    function handleKeyRelease(event) {
      ponggamefieldRef.value.handleKeyRelease(event);
    }
    // event listeners
    onMounted(() => {
      document.addEventListener('fullscreenchange', updateFullscreen);
      window.addEventListener('keydown', handleKeyPress);
      window.addEventListener('keyup', handleKeyRelease);
    });
    // remove event listeners
    onUnmounted(() => {
      document.removeEventListener('fullscreenchange', updateFullscreen);
      window.removeEventListener('keydown', handleKeyPress);
      window.removeEventListener('keyup', handleKeyRelease);
    });

    return {
      openFullscreen,
      closeFullscreen,
      modalRef,
      ponggamefieldRef,
      fullscreen,
      openModal,
      closeModal,
      handleKeyPress,
      handleKeyRelease,
    }
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
