const state = {
  allStates: [],
  current: {
    cities: {},
    events: []
  },
  actions: [],
  pathogens: [],
  finished: false
};

const getters = {
  getGameState: state => state.current,
  getNumStates: state => state.allStates.length,
  getPathogens: state => state.pathogens
};

const mutations = {
  addNewRound: (state, roundState) => {
    if (roundState.outcome !== 'pending')
      state.finished = true;
    if (roundState.round === 1)
      while (state.allStates.length)
        state.allStates.pop();

    const pathogens = (roundState.events || [])
      .filter(e => e.type === 'pathogenEncountered')
      .map(e => e.pathogen);
    state.pathogens = pathogens;
    state.allStates.push(roundState);
    state.current = roundState;
  }
};

export default {
  state, getters, mutations
};
