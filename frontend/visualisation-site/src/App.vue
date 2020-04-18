<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h3>BDS Group 27</h3>
    </v-app-bar>
    <v-content>
      <VisualiserWordCloud/>
    </v-content>
  </v-app>
</template>

<script>

// import VisualiserSentimentDistribution from "./components/VisualiserSentimentDistribution";
// import VisualiserWordDistribution from "./components/VisualiserWordDistribution";
import VisualiserWordCloud from "./components/VisualiserWordCloud";

export default {
  name: 'App',

  components: {
    VisualiserWordCloud
  },

  data: () => ({
    //
  }),
};
</script>
