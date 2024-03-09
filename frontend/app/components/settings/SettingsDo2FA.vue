<template>
	<div v-if="openPopup" class="popup">
		<div class="overlay">
			<div class="dialog">
			<div v-if="message" class="alert alert-success" role="alert">{{ message }}</div>
			<div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
			<div class ="header">
				<h2>Enable 2FA authentication</h2>
				<button type="button" class="btn-close" @click="$emit('close-popup')" aria-label="Close"></button>
			</div>
			<p>Please scan the QR code with your google authenticator app and enter the code it generates.</p>
			<div style="display: flex; align-items: center; gap: 20px; justify-content: center">
				<img :src="qrCodeUrl" alt="QR Code to activate 2 factor authentication">
				<div class="nes-field">
					<input v-model="code" type="text" id="code" class="nes-input" placeholder="Enter code">
				</div>
			</div>
			<button type="button" class="btn nes-btn" @click="enable2FA">Enable</button>
			</div>
		</div>
	</div>
</template>
  
<script>
import { ref, onMounted, watch } from 'vue';

export default {
	props: ['openPopup'],
	setup(props) {
		const code = ref('');
		const qrCodeUrl = ref('');
		const message = ref('');
		const error = ref('');

		const generateQRCode = async () => {
			try {
				const response = await fetch('/endpoint/api/qr_code', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (!response.ok) {
					const errorData = await response.json();
					error.value = errorData.error;
					message.value= '';
				}

				const data = await response.json();
				qrCodeUrl.value = `data:image/png;base64,${data.qr_code}`;
				message.value = '';
				if (data.error)
					error.value = data.error;
				else
					error.value = '';
			} catch (error) {
				message.value = '';
				error.value=error;
			}
		};

		onMounted(generateQRCode);

		const enable2FA = async() => {
			try {
				const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value;
				const response = await fetch('endpoint/api/enable_2fa', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': csrfToken,
						},
						body: JSON.stringify({
							code: code.value,
							}),
					});

				if (!response.ok) {
					error.value = 'Failed to enable 2FA, maybe the token is invalid or expired';
					throw new Error('Failed to enable 2FA');
				}

				const data = await response.json();
				if (data.success && !data.error) {
					message.value = '2FA enabled successfully';
					error.value='';
				} else {
					message.value='';
					error.value = data.error;
				}
			} catch (error) {
				error.value = error;
				message.value = '';
			}
		};

		return {
			code,
			qrCodeUrl,
			enable2FA,
			error,
			message
		};
	},
};
</script>

<style>

.dialog {
	position: relative;
}

.header {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}

.btn-close {
    position: absolute;
    right: 10px;
    top: 10px;
	top: 5px;
}
</style>