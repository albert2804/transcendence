<template>
	<div>
	</div>
</template>

<script>
	export default 
	{
		created() 
		{
			if(process.client)
			{
				const urlParams = new URLSearchParams(window.location.search);
				const redirectTo = urlParams.get('to');
				if (redirectTo) 
				{
					this.$router.push(redirectTo);
				}
			}
		}
	};
</script>