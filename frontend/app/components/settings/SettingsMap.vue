<template>
  <div v-if="openPopup" class="popup">
    <div class="map_container">
      <div class="map_item" v-for="(mapUrl, index) in mapUrls" :key="index" @click="selectMap(mapUrl)">
        <img :src="mapUrl" alt="Map" class="map_image" />
      </div>
    </div>
    <button type="button" @click="cancelChanges()" class="btn-close" aria-label="Close"></button>
  </div>
</template>

  <script>
export default {
  props: {
    openPopup: Boolean
  },
  data(){
		return {
			mapUrls: [
        'https://as1.ftcdn.net/v2/jpg/05/62/67/14/1000_F_562671472_15eURCB3BIsBsDRTe208yj81EdEJ3pfZ.jpg',
        'https://wallpapercave.com/wp/6nBenYi.jpg',
        'https://img.freepik.com/premium-vector/abstract-seamless-line-pattern-design-simple-graphic-design-fabric-print_754623-288.jpg?w=2000',
        'https://img.freepik.com/premium-vector/vertical-stripes-parallel-straight-monochrome[…]lftone-gradient-line-pattern-background_833685-828.jpg?w=2000',
        'https://c4.wallpaperflare.com/wallpaper/824/904/933/42-the-hitchhiker-s-guide-to-the-galaxy-wallpaper-preview.jpg',
		  ],
			map: '',
			error: '',
		};
	},

	methods: {
		async saveChanges() {
			try {
		    const csrfToken = useCookie('csrftoken', { sameSite: 'strict' }).value
			const response = await fetch('/endpoint/user/info/', {
        		method: 'POST',
          		headers: {
            	'Content-Type': 'application/json',
            	'X-CSRFToken': csrfToken,
          	    },
				body: JSON.stringify({ newMap: this.map })
       		 })
			 if (response.ok){
				this.closePopup();
			 }
			 	console.log("Changed username/map worked");
			} catch (error) {
				console.error('Error updating user alias/map:', error);
			}
		},

		cancelChanges() {
      this.map = '';
			this.saveChanges();
    },

		closePopup() {
			this.$emit('close-popup');
		},
		
		async selectMap(mapUrl) {
			this.map = mapUrl;
			this.saveChanges();
		}
	},
}
</script>

<style>
  .card-size {
    max-width: 400px;
  }

  .map_container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 10px;
  }

  .map_item img {
    width: 100%;
    height: auto;
  }

  .shade-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(255,255,255,0.7);
  }

  .popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-height: 100vh;
    overflow: auto;
	}
</style>
