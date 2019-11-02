import io from 'socket.io-client';
import Vue from 'vue';
import MainWindow from './components/Main';
import store from './stores';

Vue.config.productionTip = false;
Vue.config.devtools = false;

Vue.prototype.$socket = window.socket = io.connect('http://localhost:50123');

new Vue({
  el: '#app',
  store,
  render: (h) => h(MainWindow)
});
