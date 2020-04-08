from typing import Callable

from data_gathering.query_param_mapping import QueryParamsToFetchersPipeline
from data_gathering.statuses_fetch import FetchersToStatuses
from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep, SpreadPipelineStep, MergePipelineStep, \
    SplitPipelineStep
from processing.post_processing.SentimentDistributionPipeline import SentimentDistributionPipeline
from processing.sentiment_analysis.preprocessing_step import LowerCasePreprocessingPipeline, \
    RemoveNumberPreprocessingPipeline, \
    RemoveUrlPreprocessingPipeline, RemovePunctuationPreprocessingPipeline, RemoveWhiteSpacePreprocessingPipeline, \
    PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from processing.utils.flatten_pipeline import FlattenPipeline
from processing.utils.list_pipelines import CountPipeline, MaxPipeline, GetAtIndexPipeline
from processing.utils.map_pipeline import MapPipeline
from processing.utils.statuses_to_json_pipeline import StatusesToJsonPipeline
from processing.utils.extract_tweet_from_json import ExtractTweetFromJson


def _sentiment_analysis_pipeline():
    input_step = InputPipelineStep()
    output = input_step \
        .link(QueryParamsToFetchersPipeline('query_params_mapping', checkpointed=True)) \
        .link(FetchersToStatuses('fetch_data', checkpointed=True)) \
        .link(FlattenPipeline('flatten_data')) \
        .link(StatusesToJsonPipeline('to_json')) \
        .link(ExtractTweetFromJson('extract_tweet')) \
        .link(SpreadPipelineStep(do_async=True)) \
        .link(LowerCasePreprocessingPipeline('lower_data')) \
        .link(RemoveUrlPreprocessingPipeline('remove_url')) \
        .link(RemoveNumberPreprocessingPipeline('remove_n')) \
        .link(RemovePunctuationPreprocessingPipeline('remove_punct')) \
        .link(RemoveWhiteSpacePreprocessingPipeline('remove_space')) \
        .link(SentimentAnalysisPipeline('sentiment', checkpointed=True))
    return input_step, output


def get_sentiment_analysis_pipeline(callback: Callable):
    """Gets the pipeline that is used for untargeted sentiment analysis"""
    input, output = _sentiment_analysis_pipeline()
    output \
        .link(MergePipelineStep()) \
        .link(OutputPipelineStep('output_sentiment', callback))
    return input


def only_class(x):
    return x[0]


def get_sentiment_analysis_distribution_pipeline(callback: Callable):
    """Gets the pipeline that is used for untargeted sentiment analysis"""
    input, output = _sentiment_analysis_pipeline()

    output \
        .link(MergePipelineStep()) \
        .link(MapPipeline('only_class', func=only_class)) \
        .link(SentimentDistributionPipeline('sentiment_distribution')) \
        .link(OutputPipelineStep('output_sentiment_distribution', callback))
    return input


def key_val_to_tuple(x):
    return x


def get_sentiment_analysis_most_prevalent_pipeline(callback: Callable):
    """Gets the pipeline that is used for untargeted sentiment analysis"""
    input, output = _sentiment_analysis_pipeline()

    output \
        .link(MergePipelineStep()) \
        .link(MapPipeline('only_class', func=only_class)) \
        .link(CountPipeline()) \
        .link(GetAtIndexPipeline(index=0)) \
        .link(OutputPipelineStep('output_most_prevalent_sentiment', callback))
    return input


def get_json_from_tweets(callback: Callable):
    """Gets the pipeline that is used for untargeted raw data retrieval"""
    input_step = InputPipelineStep()  # Input is the query params
    input_step \
        .link(QueryParamsToFetchersPipeline('query_params_mapping', checkpointed=True)) \
        .link(FetchersToStatuses('fetch_data', checkpointed=True)) \
        .link(FlattenPipeline('flatten_data')) \
        .link(StatusesToJsonPipeline('to_json')) \
        .link(OutputPipelineStep('output_raw', callback, checkpointed=True))
    return input_step
