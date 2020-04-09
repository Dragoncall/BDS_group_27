<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h3>BDS Group 27</h3>
    </v-app-bar>
    <v-content>
      <v-container>
        <VisualiserSentimentDistribution/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>

import VisualiserSentimentDistribution from "./components/VisualiserSentimentDistribution";

export default {
  name: 'App',

  components: {
    VisualiserSentimentDistribution
  },

  data: () => ({
    //
  }),
};
</script>
