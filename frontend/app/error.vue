<template>
    <div class="container vh-80 is-centered">
      <div class="d-flex justify-content-center align-items-center" style="height: 75%;">
        <div class="nes-container is-rounded with-title is-centered">
          <p class="title" style="font-size: 2.5em;">{{ error.statusCode }}</p>
          <p>{{ error.message }}</p>
          <i class="bi bi-emoji-dizzy" style="font-size: 2.5em;"></i>
        </div>
      </div>
      <button type="button is-centered" class="nes-btn"
      @click="$router.go(-1)">Go Back</button>
    </div>
</template>

<script>
  import { defineComponent } from 'vue'

  export default defineComponent({
    props: {
      error: {
        type: Object,
        required: true
      }
    },
  })
</script>