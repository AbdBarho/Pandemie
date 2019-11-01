<template lang="pug">
div#MainWindow
  .gameState
    JSONRenderer.no-select(name='Game State' :value='gameState')

</template>

<script>
import { mapGetters } from "vuex";
import JSONRenderer from "./JSONRenderer";

export default {
  computed: mapGetters({
    gameState: "getGameState"
  }),
  components: { JSONRenderer }
};
</script>

<style lang="scss" scoped>
#MainWindow {
  width: 100%;
  height: 100%;
}
.no-select {
  // user-select: none;
}
.gameState {
  padding: 30px;
}
</style>
