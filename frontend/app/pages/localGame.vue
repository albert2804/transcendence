<template>
    <div>
      <div style="justify-content: center; margin-top: 20vh;">
        <LocalPong ref="pongComponentRef" @updateIsGameWon="isGameWon = $event"/>
        <LocalTournament @startGame="callStartGame" :isGameWon="isGameWon" />
      </div>
    </div>
  </template>

  <script>
  export default {
    methods: {
      callStartGame() {
        this.$refs.pongComponentRef.startGame();
      },
    },
  };
</script>