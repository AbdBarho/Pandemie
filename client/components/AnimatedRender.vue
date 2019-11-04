<template lang="pug">
transition(name='bounce')
  slot(v-if='shouldRender')
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters(["shouldRender"]),
  }
};
</script>

<style lang='scss' scoped>
.bounce-enter-active {
  animation: bounce-in 100ms;
}
.bounce-leave-active {
  animation: bounce-in 100ms reverse;
}
@keyframes bounce-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
