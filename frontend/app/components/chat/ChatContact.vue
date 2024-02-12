<template>
	<div class="icon-container">
		<div v-if="unreadMessageCountMap.get(String(user.id)) != 0">
			<span class="badge rounded-pill bg-danger">
				{{ unreadMessageCountMap.get(String(user.id)) }}
			</span>
		</div>
		<span style="width: 5px; display: inline-block;"></span>
		<div v-if="user.is_friend" class="friends-icon">
			<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#007bff" class="bi bi-star-fill" viewBox="0 0 16 16">
				<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
			</svg>
		</div>
		<div v-if="user.blocks" class="blocked-icon">
			<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" class="bi bi-x-circle" viewBox="0 0 16 16">
				<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
				<path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
			</svg>
		</div>
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