<template lang="pug">
div#MainWindow
  //- h1 Pandemie
  .pageContent
    .column(style='width: 45%')
      div
        Overview
        Tabs
    .column(style='width: 55%')
      div
        AnimatedRender
          Cities
          //- JSONRenderer.no-select(v-if='show' name='Cities' :value='gameState.cities')

</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";
import Cities from "./Cities";
import AnimatedRender from "./AnimatedRender";
// import Control from "./Control";
import Overview from './Overview'
import Tabs from './Tabs';

export default {
  computed: {
    ...mapGetters({ gameState: "getGameState" })
  },
  components: { JSONRenderer, Cities, AnimatedRender,  Overview, Tabs }
};
</script>

<style lang="scss" scoped>
$pad: 15px;
#MainWindow {

  width: 100%;
  height: 100%;


  // padding: $pad;
  // width: calc(100% - #{2 * $pad});
  // height: calc(100% - #{2 * $pad});

  // max-width: 1400px;
  // margin: 0 auto;

  // user-select: none;
  // display: flex;
  // flex-flow: column;
}

.pageContent {
  box-sizing: border-box;
  height: calc(100%);
  width: 100%;
  // flex: 1;
  // display: flex;
}
.column {
  // flex-basis: 0;
  // flex: 1;
  // height: calc(100% - #{2 * $pad});
  float: left;
  height: 100%;
  outline: 1px solid white;
  & > div {
    box-sizing: border-box;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
  }
}
</style>
