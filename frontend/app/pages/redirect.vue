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
				const error = urlParams.get('error');
				if (redirectTo)
					this.$router.push({ name: redirectTo, query: { error: error } });
			}
		}
	};
</script>