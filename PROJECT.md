# Person Sentiment Analysis
## Project Big Data Science | Group 27

This project aims to search the sentiment of a couple of optimised prominent people based on what people are tweeting about them.
This over time ranges as given by the user and with extra possible queries, such as count,
relevancy_type, geocode, ...

The twitter API is mirrored as closely as possible to allow easy entry for people with previous experience.
This project can thus be seen as an augmentation/wrapper of the twitter API with sentiment analysis and other augments.

This project was written in a pipeline structure to allow quick reuse and reassembly of individual steps.
We encourage collaborators to implement their own pipelines and expand our pipeline zoo!

### Current endpoints

- /: Returns this file as formatted html ( Hello there! :) )
- /raw-data: Returns the raw data as retrieved from the Twitter API
- /sentiment-data: Returns the sentiment data over the retrieved Tweets
- /sentiment-distribution: Returns the distribution of the sentiments of all tweets 
- /most-prevalent-sentiment: Returns the most prevalent sentiment
- /word-distribution: Returns the distribution of the most frequent word occurrences in the tweets (20)
- /word-cloud: Returns the full word occurrence distribution to be used in word clouds
- /sentiment-history: Returns the offline fetched data over multiple dates
  - Small note, this has only been set up locally. If this enters production, a cron-job service should be set up.

### Current query parameters

- query: Search query for the tweets
- lang:  Language of the tweets
- count: Amount of tweets retrieved
- until: Tweets until date
- since_id: Only tweets after a given tweet
- max_id: Only tweets before a given tweet
- filter_retweets: Filter retweets

### API Examples
`/wordcloud?query=kek&count=1`

`/word-distribution?query=kek&count=1`

`/sentiment-data?query=kek&count=1`

`/sentiment-distribution?query=kek&count=1`

`/raw-data?query=kek&count=1`

`/sentiment-history?figure=POTUS&result_type=recent`

## Optimised handles
Some prominent figures were focused on by our team for analysis. These people contain extra tags and keywords used
a lot to depict them or reference them. We accept augmentations to these people. This can be done by adding or changing
keywords in the `prominent_people.json` file on our github.  

Optimised prominent people include:

- POTUS (currently Donald Trump) (USA)
- Elon Musk (Business)
- Bill Gates (Business)
- Boris Johnson (UK)
- Sanchez Castejon (Spain)
- Justin Trudeau (Canada)
- Emmanuel Macron (FR)

More can be found or added in the `resources/prominent_people.json` file.