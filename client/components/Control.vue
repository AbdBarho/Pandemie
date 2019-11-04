<template lang="pug">
  div
    Overview
    Tabs
    //- AnimatedRender
      JSONRenderer(name="Events" :value='gameState.events')
</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";
import Overview from "./Overview";
import Cities from "./Cities";
import AnimatedRender from './AnimatedRender';
import Tabs from './Tabs';

export default {
  computed: {
    ...mapGetters({gameState: "getGameState"}),
  },
  components: { JSONRenderer, Overview, Cities, AnimatedRender, Tabs }
};
</script>

<style lang='scss' scoped>

.send {
  position: sticky;
  float: right;
  top: 5px;
}
</style>
