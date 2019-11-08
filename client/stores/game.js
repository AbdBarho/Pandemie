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
  vaccinesInDevelopment: [],
  availableVaccines: [],
  medicationsInDevelopment: [],
  availableMedications: [],
  finished: false
};

const getters = {
  getFirst: state => state.first,
  getFirstTotalPopulation: state => state.totalPopulationFirst,
  getGameState: state => state.current,
  getRound: state => state.current.round,
  getPathogens: state => state.pathogens,
  getActions: state => state.actions,
  getGameFinished: state => state.finished,
  getVaccinesInDevelopment: state => state.vaccinesInDevelopment,
  getAvailableVaccines: state => state.availableVaccines,
  getMedicationsInDevelopment: state => state.medicationsInDevelopment,
  getAvailableMedications: state => state.availableMedications,
};

const mutations = {
  addNewRound: (state, roundState) => {
    state.finished = roundState.outcome !== 'pending';

    if (roundState.round === 1) {
      state.first = roundState;
      state.totalPopulationFirst = Object.values(roundState.cities)
        .reduce((acc, cur) => acc + cur.population, 0);
    }
    const events = (roundState.events || []);
    state.pathogens = events.filter(e => e.type === 'pathogenEncountered')
      .map(e => e.pathogen);

    state.vaccinesInDevelopment = events.filter(e => e.type === 'vaccineInDevelopment')
      .map(e => e.pathogen.name);

    state.availableVaccines = events.filter(e => e.type === 'vaccineAvailable')
      .map(e => e.pathogen.name);

    state.medicationsInDevelopment = events.filter(e => e.type === 'medicationInDevelopment')
      .map(e => e.pathogen.name);

    state.availableMedications = events.filter(e => e.type === 'medicationAvailable')
      .map(e => e.pathogen.name);


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
