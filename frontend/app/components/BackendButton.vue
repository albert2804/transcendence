<template>
  <div class="center">
    <b-button variant="primary" @click="fetchData">
      Click me!
    </b-button>
    <b-modal v-model="showModal" title="Response from Django API:" hide-footer>
      <ul>
        <li v-for="(value, key) in data" :key="key">
          {{ key }}: {{ value }}
        </li>
      </ul>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'BackendButton',
  data () {
    return {
      data: null,
      showModal: false
    }
  },
  methods: {
    fetchData () {
      fetch('/endpoint/api/test')
        .then(response => response.json())
        .then((data) => {
          this.data = data
          this.showModal = true
        })
        .catch(error => console.error('Error:', error))
    }
  }
}
</script>

<style scoped>
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
