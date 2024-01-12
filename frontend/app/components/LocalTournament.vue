<template>
  <div class="formTournament">
    <!-- Toggle button -->
    <button @click="toggleForm" class="start-tournament">
      {{ formVisible ? 'No Tournament' : 'Local Tournament' }}
    </button>

    <!-- Form (shown/hidden based on formVisible) -->
    <div v-if="formVisible" class="formTournament">
      <form> 
        <label for="nbrPlayerRange" class="form-label">Number of total Players</label>
          <div class="mb-3 d-flex align-items-center">
            <input type="range" class="form-range" min="3" max="42" id="nbrPlayerRange" v-model="nbr_players">
            <input type="number" class="form-control" v-model.number="nbr_players" min="3" max="42">
          </div>
          <div class="name-box">
            <div v-for="index in nbr_players" :key="index" class="name-input">
              <label :for="'name' + index" class="form-label">Player {{ index }}:</label>
              <input :id="'name' + index" type="text" class="form-input" v-model="all_players[index - 1]">
            </div>
          </div>
          <button type="submit" @click="startTournament" class="start-tournament">Start Tournament</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      all_players: [
        {
          name: '',
          games_won: '[]',
        },
      ],
      nbr_players: '3',
      formVisible: false,
    };
  },
  mounted() {
    
  },
  methods: {
    toggleForm() {
      this.formVisible = !this.formVisible;
      console.log(this.formVisible);
    },
    startTournament() {
      // Implement logic to start the tournament
      // You can add more logic here as needed
      // For now, just toggle the form visibility
      this.formVisible = false;
    },
  },
};
</script>

<style scoped>
	.start-tournament{
    display: flex;
    margin: 10px auto; /* Center the button horizontally */
    padding: 10px;
    font-size: 16px;
    height: 50px;
	}

  .formTournament {
    width: 800px;
    margin: auto;
  }

  .form-range {
    width: 650px;
  }

  .form-control {
    width: 100px;
    margin-left: 50px;
  }

  .name-box {
    display: flex;
    max-width: 800px;
    flex-wrap: wrap;
  } 

  .name-input {
    max-width: 400px;
    margin: 5px;
  }

</style>
