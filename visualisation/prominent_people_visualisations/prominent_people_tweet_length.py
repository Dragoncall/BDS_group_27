from collections import defaultdict
from typing import List, Union

from tweepy import Status

from data_gathering.statuses_fetch import FetchersToStatuses
from models.prominent_person import ProminentUser
from models.result_types import ResultType
from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep, SplitPipelineStep, SpreadPipelineStep, \
    PrintPipelineStep
from processing.models.prominent_person_compile_pipeline import ProminentPersonCompilePipeline, \
    ProminentPersonCompileOnArgsPipeline
from processing.sentiment_analysis.preprocessing_step import PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from processing.utils.fetcher_augmenter import FetcherAugmenter
from processing.utils.flatten_pipeline import FlattenPipeline
from settings import get_tweepy_client
from visualisation.pipelines.visualiser import Visualiser
import matplotlib.pyplot as plt

from visualisation.prominent_people_visualisations.pipelines import default_prominent_people_pipeline, \
    run_prominent_people_pipeline


class ProminentPeopleVisualiser(Visualiser):
    # This example plots the word count per tweet
    def visualise(self, tweets: 'List[Status]'):
        text_list = []
        for tweet in tweets:
            if hasattr(tweet, 'full_text'):
                text_list.append(tweet.full_text)
            else:
                text_list.append(tweet.text)

        binned_wordcounts = defaultdict(list)
        for text in text_list:
            binned_wordcounts[len(text)].append(text)
        plt.bar(
            list(binned_wordcounts.keys()),
            [len(binned_wordcounts[key]) for key in binned_wordcounts.keys()]
        )
        plt.show()


def get_tweet_length_pipeline():
    # Combine Pipelines to get the required result
    input_step = default_prominent_people_pipeline()
    input_step \
        .link(FetcherAugmenter('augment_fetchers_count_result_type', {'count': 100, 'result_type': ResultType.POPULAR})) \
        .link(FetchersToStatuses('fetch_data')) \
        .link(FlattenPipeline('flatten_data')) \
        .link(ProminentPeopleVisualiser()) \
        .link(OutputPipelineStep('output', lambda x: print(f'length: {len(x)}')))
    return input_step


if __name__ == '__main__':
    run_prominent_people_pipeline(
        get_tweet_length_pipeline(),
        ['POTUS', 'Sophie_Wilmes', 'EmmanuelMacron']
    )
