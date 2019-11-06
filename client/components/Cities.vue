<template lang="pug">
table
  thead
    tr
      th.pointer(v-for='(label, i) in labels' :key='label' :title='firstUpper(keys[i])'
        @click='sort(keys[i])'
      ) {{ label + ( sortedBy !== keys[i] ? "\u00A0\u00A0": (asc ? '\u2b9f': '\u2b9d') ) }}
  tbody
    tr(v-for='city in cities' :key='city[0]' :class='{active: selectedCity === city[0]}'
    @click='selectCity(city[0])'
    @dblclick='goToCityTab')
      td(v-for='(prop, i) in city' :key='city[0] + keys[i]' )
        span.value(:data-type='typeof prop' :data-content='prop' :data-key='keys[i]')
          | {{ prop }}
</template>


<script>
import { mapGetters } from "vuex";

const GRADE_TO_NUMBER = {
  "--": 0,
  "-": 1,
  o: 2,
  "+": 3,
  "++": 4
};
export default {
  name: "Cities",
  data() {
    return {
      sortedBy: 'events',
      asc: false
    };
  },
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
      const cities = Object.values(this.gameState.cities).map(city => {
        const output = [];
        for (const key of this.keys) {
          if (key === "connections" || key === "events")
            output.push((city[key] || []).length);
          else output.push(city[key]);
        }
        return output;
      });
      if (this.sortedBy === 'name')
        return cities.sort((a, b) => this.asc ? a[0].localeCompare(b[0]): b[0].localeCompare(a[0]));


      const index = this.keys.indexOf(this.sortedBy);
      if(this.sortedBy === 'population' || this.sortedBy === 'connections' || this.sortedBy === 'events')
        return cities.sort((a, b) => this.asc ? a[index] - b[index]: b[index] - a[index])

      console.log(this.sortedBy, this.keys.indexOf(this.sortedBy))
      return cities.sort((a, b) => {
        const aVal = GRADE_TO_NUMBER[a[index]];
        const bVal = GRADE_TO_NUMBER[b[index]];
        return this.asc ? aVal - bVal : bVal - aVal;
      });
    }
  },
  methods: {
    sort(label) {
      if(this.sortedBy == label)
        this.asc = !this.asc;
      this.sortedBy = label;
    },
    firstUpper(text) {
      return text[0].toUpperCase() + text.slice(1);
    },
    selectCity(city) {
      this.$store.commit("setCity", city);
    },
    goToCityTab() {
      this.$store.commit("setControlTab", "City");
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
.pointer {
  cursor: pointer;
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

.value[data-key="connections"] {
  color: $lime;
}
.value[data-key="events"] {
  color: yellow;
}
</style>
