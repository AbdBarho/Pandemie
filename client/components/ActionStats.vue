<template lang="pug">
table.stats
  thead
    tr
      th
      th Medication
      th Vaccine
  tbody
    tr(v-for='pathogen in pathogenNames' :key='pathogen.name')
      td {{ pathogen.name }}
      td(:data-content='pathogen.med') {{ pathogen.med }}
      td(:data-content='pathogen.vac') {{ pathogen.vac }}

</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters({
       vacInDev: "getVaccinesInDevelopment", avVac: "getAvailableVaccines",
       medInDev: "getMedicationsInDevelopment", avMed: "getAvailableMedications",
       pathogens: "getPathogens",
    }),
    pathogenNames(){
      const names =  this.pathogens.map(p => p.name);
      return names.map(name => ({
        name,
        med: this.medInDev.includes(name) ? 'development': this.avMed.includes(name) ? "ready": "",
        vac: this.vacInDev.includes(name) ? 'development': this.avVac.includes(name) ? "ready": ""
      }))
    }
  }
};
</script>

<style lang="scss" scoped>
table.stats {
  background-color: inherit;
  td:first-of-type{
    text-align: left;
  }
  th, td {
    width: calc(100% / 3);
    border: 1px solid white;
    padding: 5px;
  }
  td[data-content='development']{
    background-color: rgba(255, 239, 12, 0.384)
  }

  td[data-content='ready']{
    background-color: rgba(117, 250, 76, 0.5)
  }
}
</style>
