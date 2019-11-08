<template lang="pug">
table
  thead
    th Outcome
    th Round
    th Points
    th Percent Alive
  AnimatedRender
    tbody
      td.value(data-type='string' :data-content='outcome' data-key='outcome') {{ outcome }}
      td.value(data-type='number' data-key='round') {{ round }}
      td.value(data-type='number' :data-content='points' data-key='points') {{ points }}
      td.value(data-type='number' :data-content='percentLiving' data-key='percentLiving') {{ percentLiving }}



</template>


<script>
import { mapGetters } from "vuex";
import AnimatedRender from './AnimatedRender';
export default {
  name: "Overview",
  computed: {
    ...mapGetters({ gameState: "getGameState" , totalFirst: "getFirstTotalPopulation"}),
    outcome() {
      return this.gameState.outcome;
    },
    points() {
      return this.gameState.points;
    },
    round(){
      return this.gameState.round;
    },
    percentLiving(){
      const current = Object.values(this.gameState.cities).reduce((acc, cur) => acc + cur.population, 0);
      return (current / this.totalFirst * 100).toFixed(1)
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
