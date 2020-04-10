<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h3>BDS Group 27</h3>
    </v-app-bar>
    <v-content>
      <VisualiserWordDistribution/>
    </v-content>
  </v-app>
</template>

<script>

// import VisualiserSentimentDistribution from "./components/VisualiserSentimentDistribution";
import VisualiserWordDistribution from "./components/VisualiserWordDistribution";

export default {
  name: 'App',

  components: {
    VisualiserWordDistribution
  },

  data: () => ({
    //
  }),
};
</script>
