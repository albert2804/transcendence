<template>
  <div>
    <!-- Toggle button -->
    <button @click="toggleForm" class="start-tournament">
      {{ formVisible ? 'No Tournament' : 'Local Tournament' }}
    </button>

    <!-- Form (shown/hidden based on formVisible) -->
    <div v-if="formVisible">
      <form>
        <label for="nbrPlayerRange" class="form-label">Number of total Players</label>
          <div class="mb-3 d-flex align-items-center">
            <input type="range" class="form-range" min="3" max="42" id="nbrPlayerRange" v-model="nbr_players">
            <input type="number" class="form-control" v-model.number="nbr_players" min="3" max="42">
          </div>
          <div v-for="index in nbr_players" :key="index" class="mb-3">
            <label :for="'name' + index" class="form-label">Name for Player {{ index }}</label>
            <input :id="'name' + index" type="text" class="form-control" v-model="all_players[index - 1]">
          </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
      <button @click="startTournament" class="start-tournament">Start Tournament</button>
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
    
  }
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
    margin: 10px auto; /* Center the button horizontally */
    padding: 10px;
    font-size: 16px;
	}
</style>
