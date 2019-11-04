const state = {
  allStates: [],
  current: {
    cities: {},
    events: []
  },
  actions: [],
  finished: false
};

const getters = {
  getGameState: state => state.current,
  getNumStates: state => state.allStates.length
};

const mutations = {
  addNewRound: (state, roundState) => {
    if (roundState.outcome !== 'pending')
      state.finished = true;
    if (roundState.round === 1)
      while (state.allStates.length)
        state.allStates.pop();

    state.allStates.push(roundState);
    state.current = roundState;
  }
};

export default {
  state, getters, mutations
};
