<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <h1>Sentiment Distribution</h1>
        <v-text-field label="Query" v-model="query"></v-text-field>
        <v-text-field label="Until" v-model="until"></v-text-field>
        <v-text-field type="number" label="Since ID" v-model="since_id"></v-text-field>
        <v-text-field type="number" label="Max ID" v-model="max_id"></v-text-field>
        <v-slider style="margin-top: 32px;" v-model="count" min="5" max="500" label="Count" thumb-label="always"></v-slider>
        <v-switch label="Filter retweets" v-model="filter_rt" value="True"></v-switch>
        <v-btn :loading="loading" @click="fetchData()">Fetch</v-btn>
        <ejs-chart id="container" title='sentiment distribution' v-if="data" :primaryXAxis='primaryXAxis'>
          <e-series-collection>
            <e-series :dataSource='data' type='Column' xName='x' yName='y' name='Sentiment Distribution'> </e-series>
          </e-series-collection>
        </ejs-chart>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import { ColumnSeries, Category } from "@syncfusion/ej2-vue-charts";
  const axios = require('axios').default;

  const mapping = {
    '0': 'Negative',
    '1': 'Positive',
    '2': 'Neutral'
  }

  export default {
    name: 'VisualiserSentimentDistribution',

    data: () => ({
      query: '',
      count: 20,
      until: '',
      since_id: undefined,
      max_id: undefined,
      filter_rt : '',
      data: undefined,
      primaryXAxis: {
        valueType: 'Category',
        title: 'Sentiment'
      },
      loading: false,
      url: 'http://127.0.0.1:5000/' // TODO: this is so ugly bruh
    }),
    methods: {
      async fetchData() {
        this.loading = true;
        const nonTransformedData = await axios.get(
                `${this.url}/sentiment-distribution?query=${this.query}&filter_retweets=${this.filter_rt}&count=${this.count}&until=${this.until}${this.since_id ? '&since_id=' + this.since_id : ''}${this.max_id ? '&max_id=' + this.max_id : ''}`
        );
        const values = nonTransformedData.data.sentiment_distribution;
        const data = [];
        for (const key of Object.keys(values)) {
          data.push({x: mapping[key], y: values[key]})
        }
        console.log(data);
        this.data = data;
        this.loading = false;
      }
    },
    provide: {
      chart: [ColumnSeries, Category]
    }
  }
</script>
