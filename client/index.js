import Vue from 'vue';
import MainWindow from './components/Main';
import store from './stores';

Vue.config.productionTip = false;
Vue.config.devtools = false;


new Vue({
  el: '#app',
  store,
  render: (h) => h(MainWindow)
});

// io is loaded as a script in the index.html to reduce build size
const socket = Vue.prototype.$socket = window.socket = window.io();
socket.on('newRound', data => {
  store.commit('addNewRound', data);
  store.commit('triggerRender');
});
