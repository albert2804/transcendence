<template>
  <div class="nes-container is-rounded clickable" style="background-color: #f2cf08; position: relative; text-align: center;" type="button" @click="toggleMusic">
    <i v-if="sound" class="bi bi-file-earmark-music" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
    <i v-else class="bi bi-file-earmark-music-fill" style="font-size: 2.0rem; position: absolute; transform: translate(-50%, -57%);"></i>
  </div>
</template>

<script>
import { sound } from '~/store';
export default {
  name: 'SoundButton',
  data(){
    return {
    }
  },
  methods: {
    toggleMusic() {
      if (sound.value) {
        sound.value = false;
        //sound is off
      }
      else {
        sound.value = true;
        //sound is on
      }
      console.log(sound.value);
    }
  }
}

</script>