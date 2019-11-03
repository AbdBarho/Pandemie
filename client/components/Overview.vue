<template lang="pug">
div
  div
    | Round:
    |
    span.value(data-type='number' data-key='round') {{ numStates }}
  div
    | Points:
    |
    span.value(data-type='number' :data-content='points' data-key='points') {{ points }}
  div
    | Status:
    |
    span.value(:data-type='typeof outcome' :data-content='outcome' data-key='outcome') {{ outcome }}
</template>


<script>
import { mapGetters } from "vuex";
export default {
  name: "Overview",
  computed: {
    ...mapGetters({ gameState: "getGameState", numStates: "getNumStates" }),
    outcome() {
      return this.gameState.outcome;
    },
    points() {
      return this.gameState.points;
    }
  }
};
</script>


<style lang="scss" scoped>
@import "./colors.scss";
</style>
