<!-- https://getbootstrap.com/docs/5.3/components/navbar/ -->

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">ft_transcendence</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
            <NuxtLink class="nav-link active" to="/">Home</NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/login">Login</NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/chat">Chat</NuxtLink>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Dropdown
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">Action</a></li>
              <li><a class="dropdown-item" href="#">Another action</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#">Something else here</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" aria-disabled="true">Disabled</a>
          </li>
        </ul>
        <!-- <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form> -->
      </div>
    </div>
    <!-- <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBothOptions" aria-controls="offcanvasWithBothOptions">User</button> -->
    </nav>
    <!-- <div class="offcanvas offcanvas-end" data-bs-scroll="true" tabindex="-1" id="offcanvasWithBothOptions" aria-labelledby="offcanvasWithBothOptionsLabel">
      <div class="offcanvas-body">
        <Login />
      </div>
    </div> -->
</template>

<script>
// import isLoggedin from store/index.js
// so we can use it in setup()->onMounted() to get the csrf token and auth status from django
import { isLoggedIn } from '~/store';
export default {
  name: 'NavBar',
  setup() {
    onMounted(async () => {
      // return if login status already checked
      if (isLoggedIn.value !== 2) {
        return
      }
      // initate the csrf token!
      // this calls django to create a csrf token as cookie
      // this token is needed for POST requests to django
      try {
        const response = await fetch('/endpoint/api/csrf')
      } catch (error) {
        console.error('Error:', error)
      }
      // check if user is logged in and set isLoggedIn in store/index.js
      // so other components can use or listen to it
      try {
        const response = await fetch('/endpoint/api/auth_status', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (data.authenticated) {
          isLoggedIn.value = 1
        } else {
          isLoggedIn.value = 0
        }
      } catch (error) {
        console.error('Error:', error);
        isLoggedIn.value = 0
      }
    })
  },
}
</script>