const state = {
  shouldRender: true,
  controlTab: 'Events',
  selectedCity: 'Berlin',
  citiesUI: {
    sortedBy: 'events',
    asc: false
  }
};

const getters = {
  shouldRender: state => state.shouldRender,
  controlTab: state => state.controlTab,
  getSelectedCity: state => state.selectedCity,
  getCitiesUIConfig: state => state.citiesUI
};

const mutations = {
  triggerRender: state => {
    state.shouldRender = false;
    setTimeout(() => state.shouldRender = true, 100);
  },
  setControlTab: (state, newTab) => state.controlTab = newTab,
  setCity: (state, city) => {
    state.selectedCity = city;
  },
  sortCitiesBy: (state, by) => state.citiesUI.sortedBy = by,
  sortCitiesAscending: (state, asc) => state.citiesUI.asc = asc
};

export default {
  state,
  getters,
  mutations
};
