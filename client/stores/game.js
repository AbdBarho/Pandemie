const d = require('./GameState.json');


const state = {
  gameState: d,
  actions: []
};

const getters = {
  getGameState: state => state.gameState,
};

const mutations = {
  setGameState: (state, newState) => state.gameState = newState,
};

export default {
  state, getters, mutations
};
