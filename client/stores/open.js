import Vue from 'vue';

const state = {
  open: {
    '/Game State': true
  }
};

const getters = {
  isOpen: state => name => {
    if (!Object.prototype.hasOwnProperty.call(state.open, name))
      Vue.set(state.open, name, false);

    return state.open[name];
  }
};

const mutations = {
  setOpen: (state, { name, val }) => Vue.set(state.open, name, val)
};

export default {
  state,
  getters,
  mutations
};
