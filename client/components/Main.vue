<template lang="pug">
div#MainWindow
  h1 Pandemie
  transition(name='bounce')
    .gameState(v-if='show')
      span Status: {{ outcome }}
      button.send(@click='send') {{ outcome !== 'pending' ? 'New Round' : 'Send round end' }}
      JSONRenderer.no-select(name='Game State' :value='gameState')

</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";

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
      setTimeout(() => (this.show = true), 200);
    });
  },
  methods: {
    send() {
      this.$socket.emit("actions", { type: "endRound" });
    }
  },
  computed: {
    ...mapGetters({ gameState: "getGameState" }),
    outcome() {
      return this.gameState.outcome;
    },
    round() {
      return this.gameState.round;
    }
  },
  components: { JSONRenderer }
};
</script>

<style lang="scss" scoped>
#MainWindow {
  max-width: 1000px;
  // height: 100%;
  margin: auto;
  padding: 30px;
}
.gameState {
  position: relative;
  // user-select: none;
  padding-bottom: 400px;
}
.send {
  position: sticky;
  float: right;
  top: 30px;
}

.bounce-enter-active {
  animation: bounce-in 0.2s;
}
.bounce-leave-active {
  animation: bounce-in 0.2s reverse;
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
