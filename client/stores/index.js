import Vue from 'vue';
import Vuex from 'vuex';
import GameStore from './game';
import Open from './open';

Vue.use(Vuex);
export default new Vuex.Store({
  modules: { GameStore, Open }
});
