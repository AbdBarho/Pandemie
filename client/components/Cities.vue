<template lang="pug">
table
  thead
    tr
      th(v-for='(label, i) in labels' :key='label' :title='firstUpper(keys[i])') {{ label }}
  tbody
    tr(v-for='city in cities' :key='city[0]')
      td(v-for='(prop, i) in city' :key='city[0] + keys[i]')
        span.value(:data-type='typeof prop' :data-content='prop' :data-key='keys[i]')
          | {{ prop }}
</template>


<script>
import { mapGetters } from "vuex";
export default {
  name: "Cities",
  computed: {
    ...mapGetters({ gameState: "getGameState" }),
    keys() {
      return [ "name", "population", "economy", "government", "hygiene", "awareness" ];
    },
    labels(){
      return ["Name", "Pop.", "Eco.", "Gov.", "Hyg.", "Awa."]
    },
    cities() {
      return Object.values(this.gameState.cities).map(val => this.keys.map(key => val[key]));
    }
  },
  methods:{
    firstUpper(text){
      return text[0].toUpperCase() + text.slice(1);
    }
  }
};
</script>

<style lang="scss" scoped>
@import './colors.scss';

table, tr, thead, tbody, td, th {
  border: none;
  border-width: 0;
}
$pad: 15px;
table {
  padding: $pad;
  width: 100%;
  text-align: left;
}
th {
  background-color: $background;
  position: sticky;
  top: 0px;
}
tr:hover{
  background-color: #444444;
}
</style>
