<template lang="pug">
//- div
//-   div
//-     | Round:
//-     |
//-     span.value(data-type='number' data-key='round') {{ numStates }}
//-   div
//-     | Points:
//-     |
//-     span.value(data-type='number' :data-content='points' data-key='points') {{ points }}
//-   div
//-     | Status:
//-     |
//-     span.value(:data-type='typeof outcome' :data-content='outcome' data-key='outcome') {{ outcome }}

table
  thead
    th Round
    th Points
    th Outcome
  AnimatedRender
    tbody
      td.value(data-type='number' data-key='round') {{ numStates }}
      td.value(data-type='number' :data-content='points' data-key='points') {{ points }}
      td.value(data-type='string' :data-content='outcome' data-key='outcome') {{ outcome }}



</template>


<script>
import { mapGetters } from "vuex";
import AnimatedRender from './AnimatedRender';
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
  },
  components: {AnimatedRender}
};
</script>


<style lang="scss" scoped>
@import "./styles/colors.scss";

table, tr, thead, tbody, td, th {
  border: none;
  border-width: 0;
}

table {
  padding: 15px;
  width: 100%;
  text-align: left;
}
</style>
