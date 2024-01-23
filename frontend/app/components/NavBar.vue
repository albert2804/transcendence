<!-- https://getbootstrap.com/docs/5.3/components/navbar/ -->

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">ft_transcendence</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <GameModal :modalTitle="'Game'" modalId="pongmodal" ariaLabel="A modal to play our remote Pong Game" />
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/">Home</NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/localGame">Local Game</NuxtLink>
          </li>
          <li class="nav-item">
            <!-- <NuxtLink class="nav-link active" to="/remoteGame">Remote Game</NuxtLink> -->
            <a class="nav-link active" @click="showGameModal">Remote Game</a>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/login">Login</NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/infopage">Info</NuxtLink>
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
export default {
  name: 'NavBar',
  methods: {
    showGameModal() {
      this.$nextTick(() => {
        new bootstrap.Modal(document.getElementById('pongmodal')).show();
      });
    },
  },
}
</script>