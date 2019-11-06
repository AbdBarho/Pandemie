<template lang="pug">
div
  table
    tbody
      td(v-for='name in tabs' :key='name' :class='{activeTab: controlTab == name}' @click='setActive(name)')
        | {{ name }}

  AnimatedRender
    div.content
      Actions(v-if='controlTab == "Actions"')
      JSONRenderer(
        v-else-if='controlTab == "Events"' name="Events" :value='gameState.events' :onlyChildren='true'
      )
      JSONRenderer(
        v-else-if='controlTab == "City"' :value='gameState.cities[city]' :onlyChildren='true'
      )
      JSONRenderer(
        v-else-if='controlTab == "Pathogens"' :value='pathogens' :onlyChildren='true'
      )


</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";
import AnimatedRender from "./AnimatedRender";
import Actions from './Actions'

export default {
  computed: {
    ...mapGetters({
      gameState: "getGameState",
      controlTab: "controlTab",
      city: "getSelectedCity",
      pathogens: "getPathogens"
    }),
    tabs() {
      return ["Actions", "Events", "Pathogens", "City"];
    }
  },
  methods: {
    setActive(val) {
      this.$store.commit("setControlTab", val);
    },
  },
  components: { JSONRenderer, AnimatedRender, Actions }
};
</script>

<style lang='scss' scoped>
@import "./styles/variables.scss";

table,
tr,
tbody,
thead td,
th {
  border-width: 0;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
  text-align: left;
  width: 100%;
}

td {
  position: sticky;
  box-sizing: border-box;
  padding: 5px 15px;
  border: 1px solid white;
  background-color: $active;
  cursor: pointer;
  &:first-of-type {
    border-left: none;
  }
  &:last-of-type {
    border-right: none;
  }
  &:hover {
    background-color: $hover;
  }
}

td.activeTab {
  background-color: inherit;
  border-bottom: none;
}

.content{
  padding: 15px;
}
</style>
