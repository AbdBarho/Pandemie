<template lang="pug">

div#MainWindow
  div.header
    h1 Pandemie
    button.send(@click='send') {{ outcome !== 'pending' ? 'New Round' : 'Send round end' }}
    transition(name='bounce')
      div(v-if='show')
        Overview
        JSONRenderer.no-select(name="Events" :value='gameState.events')

  .pageContent
    .column.left
      .gameState
        transition(name='bounce')
          //- JSONRenderer.no-select(v-if='show' name='Cities' :value='gameState.cities')
          Cities(v-if='show')
    .column.right

</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";
import Overview from "./Overview";
import Cities from "./Cities";

export default {
  data() {
    return {
      show: true
    };
  },
  mounted() {
    this.$socket.on("newRound", data => {
      this.show = false;
      this.$store.commit("addNewRound", data);
      setTimeout(() => (this.show = true), 150);
    });
  },
  methods: {
    send() {
      this.$socket.emit("actions", { type: "endRound" });
    }
  },
  computed: {
    ...mapGetters({ gameState: "getGameState", numStates: "getNumStates" }),
    outcome() {
      return this.gameState.outcome;
    }
  },
  components: { JSONRenderer, Overview, Cities }
};
</script>

<style lang="scss" scoped>
$pad: 15px;
#MainWindow {
  user-select: none;
  // width: calc(100% - #{2 * $pad});
  max-width: 1400px;
  height: calc(100% - #{2 * $pad});
  margin: 0 auto;
  padding: $pad;
  display: flex;
  flex-flow: column;
  .header {
    margin-bottom: 20px;
  }
}

.send {
  position: sticky;
  float: right;
  top: 5px;
}
.pageContent {
  box-sizing: border-box;
  height: calc(100% - #{2 * $pad});
  width: 100%;
  flex: 1;
  display: flex;
}
.column {
  flex-basis: 0;
  flex: 1;
  height: calc(100% - #{2 * $pad});
  outline: 1px solid white;
}
.left {
  flex: 1;
}
.gameState {
  box-sizing: border-box;
  height: calc(100%);
  // padding: $pad;
  overflow-x: hidden;
  overflow-y: auto;
}
.bounce-enter-active {
  animation: bounce-in 150ms;
}
.bounce-leave-active {
  animation: bounce-in 150ms reverse;
}
@keyframes bounce-in {
  0% {
    opacity: 0.1;
  }
  100% {
    opacity: 1;
  }
}
</style>
