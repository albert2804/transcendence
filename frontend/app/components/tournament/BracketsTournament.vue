<template>
  <div class="container mt-5">
    <div class="bracket">
      <div v-for="(round, index) in rounds" :key="index" class="round list-group">
        <div v-for="match in getMatches(round)" :key="match.id" class="match list-group-item">
          <p>Round {{ match.is_round }}, Match {{ match.game_nbr }}</p>
          <p>Left Player: {{ match.l_player.name }}</p>
          <p>Right Player: {{ match.r_player.name }}</p>
          <p>Left Score: {{ match.l_score }}</p>
          <p>Right Score: {{ match.r_score }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'BracketsTournament',
  props: ['numberOfPlayers', 'matches'],
  data() {
    return {
      // No need for additional data in this case
    };
  },
  computed: {
    rounds() {
      return Math.log2(this.numberOfPlayers);
    },
  },
  methods: {
    getMatches(round) {
      return this.matches.filter(match => match.is_round === round);
    },
  },
};
</script>

<style scoped>
.bracket {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.round {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.match {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>
