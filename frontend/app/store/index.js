// isLoggedIn is used to store the user's login status
// Index.vue gets the auth status from django (/endpoint/api/auth_status) and sets it here
// You can listen to, use, and modify this variable from any component
// see components/Login.vue for an example
export const isLoggedIn = ref(2); // 0 = not logged in, 1 = logged in, 2 = unknown (waiting)
export const userName = ref("");
export const userId = ref("");
export let sound = ref(false);

// gameButtonState stores the state of the game button ("disconnected", "connected", "loading")
export const gameButtonState = ref("disconnected");

// our alert banner watches this and shows changes for 5 seconds
export const alertMessage = ref("");