<template>
  <div v-if="loginStatus === 1">
    <div v-if="userExists === 1" class="d-flex flex-column">
      <div class="nes-container container-fluid with-title automargin" style="text-align: left;">
        <p class="title">User profile</p>
        <div class="user-info-container">
          <div class="col user-info-container">
            <UserProfilePic />
          </div>
          <div class="col user-info-container">
            <UserInfo />
          </div>
        </div>
      </div>
      <div class="user-games-history">
          <div class="nes-container container-fluid with-title vw-50 automargin" style="text-align: left;">
          <UserGameHistory />
        </div>
      </div>
    </div>
    <div v-else-if="userExists === 0" class="center-screen">
      <i class="bi bi-emoji-frown" style="font-size: 3rem;"></i>
      <h4 style="margin-top: 20px;">User does not exist.</h4>
    </div>
    <div v-else class="center-screen">
      <div class="spinner-border" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
  <div v-else-if="loginStatus === 0" class="center-screen">
    <div>
      <div class="nes-container is-rounded" style="width: 50%; margin: 0 auto;">
        <h3>Only members can see this page</h3>
      </div>
    </div>
  </div>
</template>

  <script>
  import { isLoggedIn } from '~/store';

  export default {
	name: 'UserInfoPage',
	setup() {
    const loginStatus = ref(isLoggedIn.value);
	  const userExists = ref(2); // 0 = false, 1 = true, 2 = unknown/waiting

	  async function checkUserExists() {
      const route = useRoute();
      let username = route.query.username;
      if (!username) {
        // No username provided show the user's own profile instead
        userExists.value = 1;
        return;
      }
      try {
        const response = await fetch('/endpoint/api/userexists?username=' + username, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
          const data = await response.json();
          userExists.value = data.exists ? 1 : 0;
      } catch (error) {
        console.error('Error:', error);
      }
	  }

    watchEffect(() => {
      loginStatus.value = isLoggedIn.value;
    });

    onMounted(() => {
		  checkUserExists();
	  });

	  return {
      loginStatus,
		  userExists,
      checkUserExists,
	  };
	}
  };
</script>

<style scoped>
.center-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 75vh;
}

.user-info-container {
  display: flex;
  align-items: center; 
  justify-content: center;
  width: 100%;
}
.user-games-history {
  max-width: 580px;
  width: 100%;
}

.user-games-history table {
  width: 100%;
}

.user-games-history th,
.user-games-history td {
  padding: 8px;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media screen and (max-width: 1575px) {
  .user-games-history {
    display: none;
  }
}

@media screen and (max-width: 700px) {
  .user-info-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>