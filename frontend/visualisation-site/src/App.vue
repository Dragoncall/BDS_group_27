<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
      <h3>BDS Group 27</h3>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav dense subheader>
        <v-subheader>Real-time analysis</v-subheader>
          <v-list-item-group v-model="group" active-class="primary--text text--accent-4">    
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-emoticon</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                <h3 @click="goToSentimentAnalysis()">Sentiment Distribution</h3>
              </v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-cloud</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                <h3 @click="goToWordCloud()">Wordcloud</h3>
              </v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-poll</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                <h3 @click="goToWordDistribution()">Word Distribution</h3>
              </v-list-item-title>
            </v-list-item>

          <v-divider></v-divider>

          <v-subheader>Prominent people stored history</v-subheader>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-emoticon</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                <h3 @click="goToSentimentHistory()">Sentiment Distribution</h3>
              </v-list-item-title>
            </v-list-item>
          </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <router-view />
    </v-content>
    
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
    //
  },

  methods: {
    goToSentimentAnalysis(){
      this.$router.push({name:'sentiment'})
    },
    goToWordCloud(){
      this.$router.push({name:'wordcloud'})
    },
    goToWordDistribution(){
      this.$router.push({name:'word-distribution'})
    },
    goToSentimentHistory(){
      this.$router.push({name:'sentiment-history'})
    }
  },

  data: () => ({
    drawer: false,
  }),
};
</script>
