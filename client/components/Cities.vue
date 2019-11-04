<template lang="pug">
table
  thead
    tr
      th(v-for='(label, i) in labels' :key='label' :title='firstUpper(keys[i])') {{ label }}
  tbody
    tr(v-for='city in cities' :key='city[0]' :class='{active: selectedCity === city[0]}')
      td(v-for='(prop, i) in city' :key='city[0] + keys[i]' @click='selectCity(city[0])')
        span.value(:data-type='typeof prop' :data-content='prop' :data-key='keys[i]')
          | {{ prop }}
</template>


<script>
import { mapGetters } from "vuex";
export default {
  name: "Cities",
  computed: {
    ...mapGetters({
      gameState: "getGameState",
      selectedCity: "getSelectedCity"
    }),
    keys() {
      return [
        "name",
        "population",
        "economy",
        "government",
        "hygiene",
        "awareness",
        "connections",
        "events"
      ];
    },
    labels() {
      return ["Name", "Pop.", "Eco.", "Gov.", "Hyg.", "Awa.", "Con.", "Ev."];
    },
    cities() {
      return Object.values(this.gameState.cities).map(city => {
        const output = [];
        for (const key of this.keys) {
          if (key === "connections" || key === "events")
            output.push((city[key] || []).length);
          else output.push(city[key]);
        }
        return output;
      });
    }
  },
  methods: {
    firstUpper(text) {
      return text[0].toUpperCase() + text.slice(1);
    },
    selectCity(city) {
      this.$store.commit("setCity", city);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "./styles/colors.scss";

table,
tr,
thead,
tbody,
td,
th {
  border: none;
  border-width: 0;
  // border-collapse: collapse;
  border-spacing: 0;
}
$pad: 15px;
table {
  padding: 0px $pad $pad $pad;
  width: 100%;
  text-align: left;
}
th {
  background-color: $background;
  position: sticky;
  top: 0px;
}

tr:nth-child(even) {
  background: #000000;
}

tr:nth-child(odd) {
  background: #101010;
}

tr:hover {
  background-color: $hover;
}
tr.active {
  background-color: $active;
}
.value[data-content="0"] {
  &[data-key="events"] {
    opacity: 0;
  }
  &[data-key="connections"] {
    opacity: 0;
  }
}

.value[data-key="connections"]{
  color: $lime;
}
.value[data-key="events"] {
  color: yellow;
}
</style>
