<template>
	<div class="icon-container">
		<div v-if="unreadMessageCountMap.get(String(user.id)) != 0">
			<span class="badge rounded-pill bg-danger">
				{{ unreadMessageCountMap.get(String(user.id)) }}
			</span>
		</div>
		<span style="width: 5px; display: inline-block;"></span>
		<div v-if="user.is_friend" class="friends-icon bi bi-star-fill" style="font-size: 1.2rem; color: #007bff;"></div>
		<div v-if="user.is_blocked" class="blocked-icon bi bi-x-circle" style="font-size: 1.2rem; color: red;"></div>
		<div v-if="user.blocks" class="blocked-icon bi bi-x-circle-fill" style="font-size: 1.2rem; color: red;"></div>
		<span class="username">{{ user.username }}</span>
	</div>
</template>

<script>
export default {
  name: 'ChatContact',
  props: {
    user: Object,
    unreadMessageCountMap: Map
  }
}
</script>

<style>
.icon-container {
  display: flex;
  align-items: center;
}
.blocked-icon,
.friends-icon {
  margin-right: 3px;
}

.username {
	margin-left: 5px;
	color: #000000;
}
</style>