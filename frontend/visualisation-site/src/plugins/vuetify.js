import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
      primary: '#2196f3',
      secondary: '#3f51b5',
      accent: '#03a9f4',
      error: '#00bcd4',
      warning: '#009688',
      info: '#4caf50',
      success: '#e91e63'
      }
    },
  },
});
