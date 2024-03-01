<template>
	<div v-if="openPopup">
		<div class="overlay">
			<div class="dialog">
			<h2>Enable 2FA</h2>
			<p>Hi {{username}}. Please scan the QR code with your authenticator app and enter the code it generates.</p>
			<img :src="qrCodeUrl" :alt="'QR Code for ' + username ">
			<input v-model="code" type="text" placeholder="Enter code">
			<button @click="enable2FA">Enable</button>
			<button @click="$emit('close-popup')">Close</button>
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

		const generateQRCode = async () => {
			try {
				const response = await fetch('/endpoint/api/qr_code', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (!response.ok) {
					throw new Error('Failed to generate QR code');
				}

				const data = await response.json();
				qrCodeUrl.value = `data:image/png;base64,${data.qr_code}`;
			} catch (error) {
				console.error('Error:', error);
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
					throw new Error('Failed to enable 2FA');
				}

				const data = await response.json();
				if (data.success) {
					alert('2FA enabled successfully');
				} else {
					alert('Failed to enable 2FA');
				}
			} catch (error) {
				console.error('Error:', error);
			}
		};

		return {
			code,
			qrCodeUrl,
			enable2FA,
		};
	},
};
</script>