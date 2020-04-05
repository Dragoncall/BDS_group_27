from collections import defaultdict
from typing import List

from tweepy import Status

from models.prominent_person import ProminentUser
from models.result_types import ResultType
from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep
from processing.sentiment_analysis.preprocessing_step import PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from settings import get_tweepy_client
from visualisation.pipelines.visualiser import Visualiser
import matplotlib.pyplot as plt


class ProminentPeopleVisualiser(Visualiser):
    # This example plots the word count per tweet
    def visualise(self, tweets:'List[Status]'):
        text_list = []
        for tweet in tweets:
            if hasattr(tweet, 'full_text'):
                print(tweet.full_text)
                text_list.append(tweet.full_text)
            else:
                print(tweet.text)
                text_list.append(tweet.text)

        binned_wordcounts = defaultdict(list)
        for text in text_list:
            binned_wordcounts[len(text)].append(text)
        plt.bar(
            list(binned_wordcounts.keys()),
            [len(binned_wordcounts[key]) for key in binned_wordcounts.keys()]
        )
        plt.show()


def get_pipeline():
    # Combine Pipelines to get the required result

    input_step = InputPipelineStep()
    input_step \
        .link(ProminentPeopleVisualiser()) \
        .link(OutputPipelineStep('output', lambda x: print('Done')))
    return input_step


def prominent_people_sentiment(prominent_person: 'ProminentUser', with_tags=True, with_keywords=True, with_handle=True):
    # 1) Setup the data gathering
    # 2) Get the pipeline
    # 3) Run with the retrieved data

    fetchers = prominent_person.compile_fetchers(with_tags, with_keywords, with_handle)
    for fetcher in fetchers:
        fetcher.set_count(100) # Use the maximum of samples
        fetcher.set_result_type(ResultType.POPULAR) # Only use the most popular tweets
    api = get_tweepy_client()
    results = [fetcher.run(api) for fetcher in fetchers]
    all_tweets = [tweet for result in results for tweet in result]
    get_pipeline().feed_data(all_tweets)

if __name__ == '__main__':
    prominent_people_sentiment(
        ProminentUser('POTUS', associated_tags=[], associated_keywords=[], api=None),
    )
