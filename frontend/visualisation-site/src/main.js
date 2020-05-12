import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'

import routes from './routes';

Vue.config.productionTip = false;

Vue.use(VueRouter)

const router = new VueRouter({routes});

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app');

import { ChartPlugin } from '@syncfusion/ej2-vue-charts';
Vue.use(ChartPlugin);

