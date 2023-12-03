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
import axios from 'axios'
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
      axios.get('/endpoint/api/test?format=json')
        .then((response) => {
          this.data = response.data
          this.showModal = true
        })
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
