<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-6">
        <h2>Ongoing Tournaments</h2>
        <select class="form-select" v-model="selectedOngoing">
          <option value="select">Select a tournament</option>
          <!-- Use v-for to dynamically generate ongoing tournament options -->
          <option v-for="tournament in ongoingTournaments" :key="tournament.id" :value="tournament.id">{{ tournament.name }}</option>
        </select>
      </div>
      
      <div class="col-md-6">
        <h2>Ended Tournaments</h2>
        <select class="form-select" v-model="selectedEnded">
          <option value="select">Select a tournament</option>
          <!-- Use v-for to dynamically generate ended tournament options -->
          <option v-for="tournament in endedTournaments" :key="tournament.id" :value="tournament.id">{{ tournament.name }}</option>
        </select>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'ListTournament',
  data() {
    return {
      selectedOngoing: 'select',
      selectedEnded: 'select',
      ongoingTournaments: [
          { id: 'tournament1', name: 'Tournament 1' },
          { id: 'tournament2', name: 'Tournament 2' },
          { id: 'tournament3', name: 'Tournament 3' }
      ],
      endedTournaments: [
          { id: 'tournament4', name: 'Tournament 4' },
          { id: 'tournament5', name: 'Tournament 5' },
          { id: 'tournament6', name: 'Tournament 6' }
      ]
    };
  },
};
</script>
