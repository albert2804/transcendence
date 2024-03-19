<template>
	<div v-if="openPopup" class="popup">
	 <div class="map_container">
      <div class="map_item" v-for="(mapUrl, index) in mapUrls" :key="index" @click="selectMap(mapUrl)">
        <img :src="mapUrl" alt="Map" class="map_image" style="width: 250px; height:175px">
      </div>
    </div>
		<button type="button" @click="saveChanges()" @keydown.escape="cancelChanges" class="btn-close" aria-label="Close"></button>
	</div>
  </template>

  <script>
export default {
  props: {
    openPopup: Boolean
  },
  data(){
		return {
			mapUrls: ['https://as1.ftcdn.net/v2/jpg/05/62/67/14/1000_F_562671472_15eURCB3BIsBsDRTe208yj81EdEJ3pfZ.jpg',
			'https://www.solidbackgrounds.com/images/1600x1200/1600x1200-bluebonnet-solid-color-background.jpg',
			'https://media1.giphy.com/media/yv1mFZ8I5jC0dXzqeU/giphy.webp?cid=790b7611vo8mc9ckck6iq56y25bwf8sy2trm5q54enxjph7t&ep=v1_gifs_search&rid=giphy.webp&ct=g',
			'https://media0.giphy.com/media/cgsGV2tVyvrhK/giphy.webp?cid=ecf05e47y5el91ponepupd5dx9pp5mziks5xfgpeaq8zxasa&ep=v1_gifs_search&rid=giphy.webp&ct=g',
			'https://c4.wallpaperflare.com/wallpaper/508/722/499/the-answer-to-life-the-universe-everything-42-everything-wallpaper-preview.jpg',
			'https://media0.giphy.com/media/RhHLT56wG7daNuwKsa/giphy.webp?cid=ecf05e47hxenonxv19e69la5npjtg292t723mqym43znos3t&ep=v1_gifs_search&rid=giphy.webp&ct=g',
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
    min-width: px;
    max-width: 400px;
  }
  .map_container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
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
  position: fixed; /* Fixed positioning to overlay on top of other content */
  top: 50%; /* Position it in the vertical center of the viewport */
  left: 50%; /* Position it in the horizontal center of the viewport */
  transform: translate(-50%, -50%); /* Center the popup exactly */
  background-color: white; /* Background color */
  padding: 20px; /* Padding around the content */
  border: 1px solid #ccc; /* Border */
  border-radius: 8px; /* Border radius */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle depth effect */
}
</style>
