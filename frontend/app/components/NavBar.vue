<!-- https://getbootstrap.com/docs/5.3/components/navbar/ -->

<template>
  <GameModal :modalTitle="'Game'" modalId="pongmodal" ariaLabel="A modal to play our remote Pong Game" />
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">ft_transcendence</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/">Home</NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active" to="/localGame">Local Game</NuxtLink>
          </li>
          <li class="nav-item">
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
      </div>
    </div>
    </nav>
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