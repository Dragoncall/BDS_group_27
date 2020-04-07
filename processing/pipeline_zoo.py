from typing import Callable

from data_gathering.query_param_mapping import QueryParamsToFetchersPipeline
from data_gathering.statuses_fetch import FetchersToStatuses
from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep, SpreadPipelineStep
from processing.sentiment_analysis.preprocessing_step import LowerCasePreprocessingPipeline, RemoveNumberPreprocessingPipeline,\
    RemoveUrlPreprocessingPipeline, RemovePunctuationPreprocessingPipeline, RemoveWhiteSpacePreprocessingPipeline, \
    PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from processing.utils.flatten_pipeline import FlattenPipeline
from processing.utils.statuses_to_json_pipeline import StatusesToJsonPipeline
from processing.utils.extract_tweet_from_json import ExtractTweetFromJson


def get_sentiment_analysis_pipeline(callback: Callable):
    """Gets the pipeline that is used for untargeted sentiment analysis"""
    input_step = InputPipelineStep()
    input_step \
        .link(QueryParamsToFetchersPipeline('query_params_mapping', checkpointed=True)) \
        .link(FetchersToStatuses('fetch_data', checkpointed=True)) \
        .link(FlattenPipeline('flatten_data')) \
        .link(StatusesToJsonPipeline('to_json'))\
        .link(ExtractTweetFromJson('extract_tweet'))\
        .link(SpreadPipelineStep())\
        .link(LowerCasePreprocessingPipeline('lower_data'))\
        .link(RemoveUrlPreprocessingPipeline('remove_url'))\
        .link(RemoveNumberPreprocessingPipeline('remove_n'))\
        .link(RemovePunctuationPreprocessingPipeline('remove_punct'))\
        .link(RemoveWhiteSpacePreprocessingPipeline('remove_space'))\
        .link(SentimentAnalysisPipeline('sentiment', checkpointed=True)) \
        .link(OutputPipelineStep('output_sentiment', callback))
    return input_step


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
