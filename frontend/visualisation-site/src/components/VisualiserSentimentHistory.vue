<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <h1>Sentiment Distribution</h1>
        <br>
        <v-select
          :items="items"
          label="Choose a prominent figure"
          v-model="figure"
          dense
        ></v-select>

        <v-radio-group v-model="result_type" row>
            <v-radio label="Recent tweets" value="recent"></v-radio>
            <v-radio label="Popular tweets" value="popular"></v-radio>
        </v-radio-group>
        <v-btn :loading="loading" @click="fetchData()">Fetch</v-btn>

        <ejs-chart id="container"
            title='Sentiment Distribution'
            v-if="data"
            :primaryXAxis='primaryXAxis'
            :legendSettings='legendSettings'
        >
          <e-series-collection>
            <e-series :dataSource='data' type='StackingArea100' xName='x' yName='y2' name='Negative'> </e-series>
            <e-series :dataSource='data' type='StackingArea100' xName='x' yName='y1' name='Neutral'> </e-series>
            <e-series :dataSource='data' type='StackingArea100' xName='x' yName='y' name='Positive'> </e-series>
          </e-series-collection>
        </ejs-chart>

      </v-col>
    </v-row>
  </div>
</template>

<script>
  import { StackingAreaSeries, Category, Legend, DateTime } from "@syncfusion/ej2-vue-charts";
  const axios = require('axios').default;

  export default {
    name: 'VisualiserSentimentHistory',

    data: () => ({
      data: undefined,
      figure: '',
      result_type: null,
      items: ['POTUS', 'BorisJohnson', 'JustinTrudeau', 'Sophie_Wilmes', 'elonmusk', 'BillGates'],
      primaryXAxis: {
        valueType: 'DateTime',
        title: 'Date',
        labelRotation : -45
      },
      legendSettings: {
          visible: true,
          position: 'Top'
        },
      loading: false,
      url: 'http://127.0.0.1:5000/' // TODO: this is so ugly bruh
    }),
    methods: {
      async fetchData() {
        this.loading = true;
        const nonTransformedData = await axios.get(
                `${this.url}/sentiment-history?figure=${this.figure}&result_type=${this.result_type}`
        );
        const values = nonTransformedData.data.sentiment_distribution;
        const data = [];
        for (const key of Object.keys(values)) {
            data.push({x: new Date(key), y: values[key]['Positive'], y1: values[key]['Neutral'], y2: values[key]['Negative']})
        }
        console.log(data);
        this.data = data;
        this.loading = false;
      }
    },
    provide: {
      chart: [StackingAreaSeries, Category, Legend, DateTime]
    }
  }
</script>
