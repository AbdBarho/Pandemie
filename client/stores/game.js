const state = {
  allStates: [],
  current: {},
  actions: []
};

const getters = {
  getGameState: state => state.current,
  getGameStatus: state => state.status,
  getAllStates: state => state.allStates
};

const mutations = {
  addNewRound: (state, roundState) => {
    state.allStates.push(roundState);
    state.current = roundState;
  }
};

export default {
  state, getters, mutations
};
