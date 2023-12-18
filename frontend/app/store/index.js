// isLoggedIn is used to store the user's login status
// Index.vue gets the auth status from django (/endpoint/api/auth_status) and sets it here
// You can listen to, use, and modify this variable from any component
// see components/Login.vue for an example
export const isLoggedIn = ref(2); // 0 = not logged in, 1 = logged in, 2 = unknown (waiting)