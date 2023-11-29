<!-- <template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style> -->

<template>
  <div class="center">
    <button class="btn btn-success" @click="fetchData">Click me</button>

    <div v-if="showModal" class="modal-background">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h1>Response from Django API:</h1>
        <ul>
          <li v-for="(value, key) in data" :key="key">
            {{ key }}: {{ value }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      data: null,
      showModal: false
    };
  },
  methods: {
    fetchData() {
      console.log('Button wurde geklickt');
      axios.get('/endpoint/api/?format=json')
        .then(response => {
          this.data = response.data;
          this.showModal = true;
        })
        .catch(error => {
          console.error('Fehler bei der API-Anfrage:', error);
        });
    },
    closeModal() {
      this.showModal = false;
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

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  width: auto;
  max-width: 80%;
  max-height: 80vh;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}
</style>