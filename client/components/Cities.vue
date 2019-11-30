<template lang="pug">
table
  thead
    tr
      th.pointer(v-for='(label, i) in labels' :key='label' :title='firstUpper(keys[i])'
        @click='sort(keys[i])'
      ) {{ label + ( sortedBy !== keys[i] ? "\u00A0\u00A0" : (asc ? '\u2b9f': '\u2b9d') ) }}
  tbody
    tr(v-for='city in cities' :key='city[0]' :class='{active: selectedCity === city[0]}'
    @click='selectCity(city[0])'
    @dblclick='goToCityTab')
      td(v-for='(prop, i) in city' :key='city[0] + keys[i]' )
        span.value(:data-type='typeof prop' :data-content='prop' :data-key='keys[i]')
          | {{ prop }}
</template>


<script>
import { mapGetters } from 'vuex';

const GRADE_TO_NUMBER = {
  '--': 0,
  '-': 1,
  'o': 2,
  '+': 3,
  '++': 4
};
export default {
  name: 'Cities',
  computed: {
    ...mapGetters({
      gameState: 'getGameState',
      firstState: 'getFirst',
      selectedCity: 'getSelectedCity',
      config: 'getCitiesUIConfig',
      pathogens: 'getPathogens'
    }),
    sortedBy(){
      return this.config.sortedBy;
    },
    asc(){
      return this.config.asc;
    },
    pathogenNames(){
      return this.pathogens.map(p => p.name);
    },
    keys() {
      let ret = [ 'name', 'population percent', 'population', 'economy', 'government', 'hygiene', 'awareness',
        'connections', 'events' ];
      for ( let idx in this.pathogenNames ){
        let pathName = this.pathogenNames[idx];
        ret = ret.concat( pathName , 'Medicinedeployed'.concat(pathName.slice(0,2)) , 'Vaccinedeployed'.concat(pathName.slice(0,2)) );
      }
      return ret;
    },
    labels() {
      let ret = [ 'Name', 'Per.', 'Pop.', 'Eco.', 'Gov.', 'Hyg.', 'Awa.', 'Con.', 'Ev.' ];
      for ( let idx in this.pathogenNames ) {
        let pathName = this.pathogenNames[idx];
        ret = ret.concat( pathName.slice(0, 4),
          'md' + pathName.slice(0, 2),
          'vd' + pathName.slice(0, 2)
        );
      }
      return ret;
    },
    cities() {
      const cities = Object.values(this.gameState.cities).map(city => {
        const output = [];
        for (const key of this.keys) {
          if (this.pathogenNames.includes(key)) {
            const hasPathogen = (city.events || [])
              .some(e => e.type === 'outbreak' && e.pathogen.name === key);
            const hasMedDeployed = (city.events || [] ).some( e => e.type ==='medicationDeployed');
            const hasVacDeployed = (city.events || [] ).some( e => e.type ==='vaccineDeployed');
            output.push(hasPathogen ? '\u25CF' : '');
            output.push(hasMedDeployed ? '\u25CF' : '');
            output.push(hasVacDeployed ? '\u25CF' : '');
          } else if (key === 'connections' || key === 'events') {
            output.push((city[key] || []).length);
          } else if (key === 'population percent') {
            output.push(
              Math.round(city.population / this.firstState.cities[city.name].population * 100)
            );
          } else {
            output.push(city[key]);
          }
        }
        return output;
      });
      const index = this.keys.indexOf(this.sortedBy);
      if (index === -1) {
        this.$store.commit('sortCitiesBy', this.keys[0]);
        return cities;
      }

      if (this.sortedBy === 'name' || this.pathogenNames.includes(this.sortedBy))
        return cities.sort((a, b) =>
          this.asc ? a[index].localeCompare(b[index]) : b[index].localeCompare(a[index])
        );

      if (numericalValues.has(this.sortedBy))
        return cities.sort((a, b) =>
          this.asc ? a[index] - b[index] : b[index] - a[index]
        );

      // console.log(this.sortedBy, this.keys.indexOf(this.sortedBy))
      return cities.sort((a, b) => {
        const aVal = GRADE_TO_NUMBER[a[index]];
        const bVal = GRADE_TO_NUMBER[b[index]];
        return this.asc ? aVal - bVal : bVal - aVal;
      });
    }
  },
  methods: {
    sort(label) {
      if (this.sortedBy === label)
        this.$store.commit('sortCitiesAscending', !this.asc);
      else
        this.$store.commit('sortCitiesBy', label);
    },
    firstUpper(text) {
      return text[0].toUpperCase() + text.slice(1);
    },
    selectCity(city) {
      this.$store.commit('setCity', city);
    },
    goToCityTab() {
      this.$store.commit('setControlTab', 'City');
    }
  }
};

const numericalValues = new Set([ 'population', 'connections', 'events', 'population percent' ]);
</script>

<style lang="scss" scoped>
@import "./styles/colors.scss";

table, tr, thead, tbody, td, th {
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
  padding: 0 $pad $pad $pad;
  width: 100%;
  text-align: left;
}

tr > td, tr > th {
  min-width: 55px;
}

th {
  background-color: $background;
  position: sticky;
  top: 0;
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
