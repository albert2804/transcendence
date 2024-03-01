<template>
	<div v-if="Popup2FA">
		<div class="overlay">
			<div class="dialog">
			<h2>Enable 2FA</h2>
			<p>Please scan the QR code with your authenticator app and enter the code it generates.</p>
			<img :src="qrCodeUrl" alt="QR Code">
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
	props: ['Popup2FA'],
	setup(props) {
		const code = ref('');
		const username = ref(''); 
		const qrCodeUrl = ref('');

		watch(() => props.Popup2FA, (newVal, oldVal) => {
			console.log('Popup2FA changed from', oldVal, 'to', newVal);
		});

		const generateQRCode = async () => {
			try {
				const response = await fetch('/api/qr-code', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
							username: username.value,
							code: code.value,
					}),
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
				const response = await fetch('/api/enable-2fa', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({
							username: username.value,
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
			username,
			qrCodeUrl,
			enable2FA,
		};
	},
};
</script>