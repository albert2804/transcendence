<template>
	<div
		:id="modalId"
		ref="modalRef"
	    class="modal fade"
	    aria-hidden="true"
	    data-bs-backdrop="static"
	    data-bs-keyboard="false"
	    style="max-height: 20vh;">
		<div class="modal" :class="{ 'show': isVisible }" tabindex="-1" role="dialog" v-if="isVisible">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">{{ modalTitle }}</h5>
						<button type="button" class="btn-close" @click="resetModal"></button>
					</div>
					<div class="modal-body">
						<!-- {{ content }} -->
						"This is my modal"
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { ref, watch } from 'vue';
// import Tournament from '~/pages/tournament.vue';
// import tournament from '~/pages/tournament.vue';

export default {
    name: 'ErrorModal',
    props: {
        isVisible: Boolean,
        content: String,
        modalTitle: String,
        modalId: {
            type: String,
            required: true,
        }
    },
    setup(props, { emit }) {
        // Use a ref to track visibility
        const isVisibleRef = ref(props.isVisible);
        // Watch for changes in the props and update the ref accordingly
        watch(() => props.isVisible, (newValue) => {
            isVisibleRef.value = newValue;
            resetModal();
        });
        const resetModal = async () => {
            // Emit an event or handle the modal reset logic if needed
            await new Promise(resolve => setTimeout(resolve, 3000));
            emit('hidden');
        };
        return {
            isVisibleRef,
            resetModal,
        };
    },
};
</script>
