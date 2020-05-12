import VisualiserWordCloud from './components/VisualiserWordCloud.vue';
import VisualiserSentimentDistribution from './components/VisualiserSentimentDistribution.vue';
import VisualiserWordDistribution from './components/VisualiserWordDistribution.vue';

const routes = [
    { 
        path: '/',
        name: 'sentiment',
        component: VisualiserSentimentDistribution
    },
    { 
        path: '/wordcloud', 
        name: 'wordcloud',
        component: VisualiserWordCloud
    },
    { 
        path: '/word-distribution',
        name: 'word-distribution',
        component: VisualiserWordDistribution 
    },
];

export default routes;