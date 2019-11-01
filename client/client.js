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
