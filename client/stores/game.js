const state = {
  first: {
    cities: {},
    events: []
  },
  totalPopulationFirst: 1,
  current: {
    cities: {},
    events: []
  },
  actions: [],
  pathogens: [],
  finished: false
};

const getters = {
  getFirst: state => state.first,
  getFirstTotalPopulation: state => state.totalPopulationFirst,
  getGameState: state => state.current,
  getRound: state => state.current.round,
  getPathogens: state => state.pathogens,
  getActions: state => state.actions,
  getGameFinished: state => state.finished
};

const mutations = {
  addNewRound: (state, roundState) => {
    state.finished = roundState.outcome !== 'pending';

    if (roundState.round === 1) {
      state.first = roundState;
      state.totalPopulationFirst = Object.values(roundState.cities)
        .reduce((acc, cur) => acc + cur.population, 0);
    }

    state.pathogens = (roundState.events || [])
      .filter(e => e.type === 'pathogenEncountered')
      .map(e => e.pathogen);

    state.current = roundState;
  },
  addAction: (state, action) => state.actions.push(action),
  removeActionByIndex: (state, index) => state.actions.splice(index, 1),
  clearActions: state => state.actions = []
};

export default {
  state,
  getters,
  mutations
};
