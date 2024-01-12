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
          <input type="range" class="form-range" min="3" max="42" id="nbrPlayerRange" v-model.number="nbr_players">
          <input type="number" class="form-control" v-model.number="nbr_players" min="3" max="42">
        </div>
        <div class="name-box">
          <div v-for="index in nbr_players" :key="index" class="name-input">
            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
              <input
                type="radio"
                class="btn-check"
                :name="radioGroupName(index)"
                :id="'btnradio1' + index"
                autocomplete="off"
                checked
                @change="setActiveRadio('Player', index)"
              />
              <label class="btn btn-outline-primary" :for="'btnradio1' + index">Player</label>

              <input
                type="radio"
                class="btn-check"
                :name="radioGroupName(index)"
                :id="'btnradio2' + index"
                autocomplete="off"
                @change="setActiveRadio('Bot', index)"
              />
              <label class="btn btn-outline-primary" :for="'btnradio2' + index">Bot</label>
            </div>
            <input :id="'name' + index" type="text" class="form-input" :value="getPlayerValue(index)">
      
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
      all_players: Array.from({ length: 42 }, () => ({
        name: '',
        games_won: '[]',
      })),
      nbr_players: '3',
      formVisible: false,
      activeRadio: 'Player',
    };
  },
  computed: {
    // Computed property to generate unique radio button group names
    radioGroupName() {
      return (index) => `btnradio${index}`;
    },
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
    setActiveRadio(value, index) {
      this.all_players[index - 1].name = value + index;
    },
    getPlayerValue(index) {
      return this.all_players[index - 1].name
    }
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
    justify-content: space-between; /* Align even elements to the right and odd elements to the left */
  }

  .name-input {
    max-width: 400px;
    margin: 5px;
  }
</style>
