<template lang="pug">
div
  template(v-if='!finished')
    ActionStats
    h4 Available Points:&nbsp;
      span.value(data-type='number' data-key='points')
        | {{available}}
        
    table
      thead
        th(v-for='name in columnNames' :key='name') {{name}}
      tbody
        tr
          td
            select(v-model='type')
              optgroup(v-for='(actions, label, index) in all' :key='label + index' :label='label')
                option(v-for='action in actions' :key='action + index' :value='action') {{action}}

          td
            input(v-show='showNumRounds' type='number' min='1' max='99' v-model='numRounds')
          td
            span(v-show='showCity') {{ city }}
          td
            select(v-show='type === "closeConnection"' v-model='toCity')
              option(v-for='neighbor in connections' :key='neighbor' :value='neighbor') {{ neighbor }}
          td
            select(v-show='showPathogen' v-model='pathogen')

              option(v-for='p in pathogenNames' :key='p' :value='p') {{ p }}

          td(:class='{error: !canAdd }') {{ cost }}
          td
            button(:disabled='!canAdd' :class='{deactivated: !canAdd}'  @click='add' title='add action') +
        tr &nbsp;
        tr
          td(style='text-align:left') Actions:
        tr(v-for='(action, index) in actions' :key='action.type + index')
          td(v-for='col in ["type", "rounds", "city", "toCity", "pathogen", "cost"]')
            template(v-if='col === "city" && !action.city') {{ action.fromCity}}
            template(v-else) {{action[col]}}
          td
            button(@click='remove(index)') x

  button.send(@click='send') {{ finished ? 'New Game' : 'Execute actions & end round' }}

</template>

<script>
import { mapGetters } from "vuex";
import ActionStats from "./ActionStats";

export default {
  components: {ActionStats},
  data() {
    return {
      type: "putUnderQuarantine",
      toCity: "",
      numRounds: 1,
      pathogen: ""
    };
  },
  methods: {
    send() {
      const actions = JSON.parse(JSON.stringify(this.actions));
      if (actions.length === 0 && !confirm("No actions selected, continue ?"))
        return;
      actions.forEach(a => delete a.cost);
      actions.push({ type: "endRound" });
      console.log(actions);
      this.$store.commit("clearActions");
      this.$socket.emit("actions", actions);
    },
    add() {
      if (!this.canAdd) return;
      const action = { type: this.type, cost: this.cost };
      if (this.type === "closeConnection") {
        action.fromCity = this.city;
        action.toCity = this.toCity;
      } else if (SHOW_CITY.has(this.type)) {
        action.city = this.city;
      }

      if (SHOW_NUM_ROUNDS.has(this.type)) {
        action.rounds = parseInt(this.numRounds);
      }

      if (SHOW_PATHOGEN.has(this.type)) {
        action.pathogen = this.pathogen;
      }
      this.$store.commit("addAction", action);
    },
    remove(index) {
      this.$store.commit("removeActionByIndex", index);
    }
  },
  computed: {
    ...mapGetters({
      city: "getSelectedCity", gameState: "getGameState", pathogens: "getPathogens",
      actions: "getActions", finished: "getGameFinished", vacInDev: "getVaccinesInDevelopment",
      avVac: "getAvailableVaccines", medInDev: "getMedicationsInDevelopment",
      avMed: "getAvailableMedications"
    }),
    cost() {
      const num = parseInt(this.numRounds);
      switch (this.type) {
        case "putUnderQuarantine":
          return 10 * num + 20;
        case "closeAirport":
          return 5 * num + 15;
        case "closeConnection":
          return 3 * num + 3;
        case "developVaccine":
          return 40;
        case "deployVaccine":
          return 5;
        case "developMedication":
          return 20;
        case "deployMedication":
          return 10;
        default:
          return 3;
      }
    },
    totalCost() {
      return this.actions.reduce((a, b) => a + b.cost, 0);
    },
    available() {
      return this.gameState.points - this.totalCost;
    },
    canAdd() {
      return (
        this.cost <= this.available &&
        (this.type !== "closeConnection" ||
          this.connections.indexOf(this.toCity) > -1) &&
        (!SHOW_PATHOGEN.has(this.type) ||
          this.pathogenNames.indexOf(this.pathogen) > -1)
      );
    },
    all() {
      return All;
    },
    connections() {
      return (this.gameState.cities[this.city] || { connections: [] }).connections;
    },
    pathogenNames() {
      if(this.type === 'developMedication')
        return this.pathogens.map(p => p.name).filter(name =>
          !this.avMed.includes(name) && !this.medInDev.includes(name)
        );
      else if (this.type === 'developVaccine')
        return this.pathogens.map(p => p.name).filter(name =>
          !this.avVac.includes(name) && !this.vacInDev.includes(name)
        );
      else if (this.type === 'deployMedication')
        return this.avMed;
      else if (this.type === 'deployVaccine')
        return this.avVac;
      else
        return [];
    },
    showCity() {
      return SHOW_CITY.has(this.type);
    },
    showNumRounds() {
      return SHOW_NUM_ROUNDS.has(this.type);
    },
    showPathogen() {
      return SHOW_PATHOGEN.has(this.type);
    },
    columnNames() {
      return COL_NAMES;
    }
  }
};
const COL_NAMES = [
  "Action Type", "Rounds", "City", "To City", "Pathogen", "Cost", ""
];

const SHOW_CITY = new Set([
  "putUnderQuarantine", "closeAirport", "closeConnection",
  "deployVaccine", "deployMedication", "exertInfluence",
  "callElections", "applyHygienicMeasures", "launchCampaign"
]);
const SHOW_NUM_ROUNDS = new Set([
  "putUnderQuarantine", "closeAirport", "closeConnection"
]);
const SHOW_PATHOGEN = new Set([
  "deployMedication", "developMedication", "deployVaccine", "developVaccine"
]);
const All = {
  Protect: ["putUnderQuarantine", "closeAirport", "closeConnection"],
  Influence: [ "exertInfluence", "callElections", "applyHygienicMeasures", "launchCampaign" ],
  Medication: ["developMedication", "deployMedication"],
  Vaccine: ["developVaccine", "deployVaccine"],
};
</script>

<style lang='scss' scoped>
@import "./styles/colors.scss";
@import "./styles/variables.scss";

table, tr, thead, tbody, td, th {
  border-spacing: 0;
}
table {
  text-align: center;
  width: 100%;
  margin-bottom: 20px;
}
th,
td {
  width: calc(100% / 6);
}

td:first-of-type {
  text-align: left;
}

tr:hover {
  background-color: $active;
}
tr:first-of-type:hover {
  background-color: inherit;
}

button,
select,
input {
  background-color: $background;
  color: $textColor;
  border: 1px solid white;
  text-align: center;
}

button {
  cursor: pointer;
  &:hover {
    background-color: $hover;
  }
  &.deactivated {
    color: $greyOut;
    cursor: initial;
    border: 1px solid $greyOut;
    background-color: $background;
    &:hover {
      background-color: $background;
    }
  }
}
.error {
  color: $red;
}
.send {
  padding: 5px;
}
.title {
  margin: 10px 0px;
}
.pad {
  padding-left: 10px;
}
</style>
