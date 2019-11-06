<template lang="pug">
div
  div Event type
  select(v-model='type')
    option(value='putUnderQuarantine') putUnderQuarantine
    option(value='closeAirport') closeAirport
    option(value='closeConnection') closeConnection
    option(value='developVaccine') developVaccine
    option(value='deployVaccine') deployVaccine
    option(value='developMedication') developMedication
    option(value='deployMedication') deployMedication
    option(value='exertInfluence') exertInfluence
    option(value='callElections') callElections
    option(value='applyHygienicMeasures') applyHygienicMeasures
    option(value='launchCampaign') launchCampaign
  //- div
    button(v-for='t of all' :key='t' @click='type=t') {{ t }}


  div(v-show='showCity') City: {{ city }}
  div(v-show='type === "closeConnection"') To City
    select(v-model='toCity')
      option(v-for='neighbor in connections' :key='neighbor' :value='neighbor') {{ neighbor }}
  div(v-show='showNumRounds')
    | Number of rounds
    input(type='number' min='1' max='99' v-model='numRounds')

  div(v-if='showPathogen') Pathogen
    select(v-model='pathogen')
      option(v-for='p in pathogens' :key='p.name' :value='p.name') {{ p.name }}

  button(@click='add') Add Action
  button(@click='send') End round
</template>

<script>

const SHOW_CITY = new Set([
  "putUnderQuarantine",
  "closeAirport",
  "closeConnection",
  "deployVaccine",
  "deployMedication",
  "exertInfluence",
  "callElections",
  "applyHygienicMeasures",
  "launchCampaign"
]);

const SHOW_NUM_ROUNDS = new Set([
  "putUnderQuarantine",
  "closeAirport",
  "closeConnection"
]);

const SHOW_PATHOGEN = new Set([
  "deployMedication",
  "developMedication",
  "deployVaccine",
  "developVaccine"
]);

const All = new Set([...SHOW_CITY, ...SHOW_NUM_ROUNDS, ...SHOW_NUM_ROUNDS])
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      type: "putUnderQuarantine",
      toCity: "",
      numRounds: 1,
      pathogen: ''
    };
  },
  methods: {
    send() {
      if (!confirm("Are u sure?")) return;
      this.$socket.emit("actions", { type: "endRound" });
    },
    add(){
      console.log(this.type, this.city,  this.toCity, this.numRounds, this.pathogen)
    }
  },
  computed: {
    ...mapGetters({
      city: "getSelectedCity",
      gameState: "getGameState",
      pathogens: "getPathogens"
    }),
    all(){
      return Array.from(All);
    },
    connections() {
      // console.log(this.city, this.gameState[this.city]);
      return this.gameState.cities[this.city].connections;
    },
    showCity() {
      return SHOW_CITY.has(this.type);
    },
    showNumRounds() {
      return SHOW_NUM_ROUNDS.has(this.type);
    },
    showPathogen() {
      return SHOW_PATHOGEN.has(this.type);
    }
  }
};
</script>

<style lang='scss' scoped>
</style>
