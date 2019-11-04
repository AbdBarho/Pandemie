const state = {
  shouldRender: true,
  controlTab: 'Events',
  selectedCity: 'Berlin'
};

const getters = {
  shouldRender: state => state.shouldRender,
  controlTab: state => state.controlTab,
  getSelectedCity: state => state.selectedCity
};

const mutations = {
  triggerRender: state => {
    state.shouldRender = false;
    setTimeout(() => state.shouldRender = true, 100);
  },
  setControlTab: (state, newTab) => state.controlTab = newTab,
  setCity: (state, city) => {
    state.controlTab = 'City';
    state.selectedCity = city;
  }
};

export default {
  state,
  getters,
  mutations
};
