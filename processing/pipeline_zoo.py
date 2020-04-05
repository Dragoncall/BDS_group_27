from typing import Callable

from data_gathering.query_param_mapping import QueryParamsToFetchersPipeline
from data_gathering.statuses_fetch import FetchersToStatuses
from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep
from processing.sentiment_analysis.preprocessing_step import PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from processing.utils.flatten_pipeline import FlattenPipeline
from processing.utils.statuses_to_json_pipeline import StatusesToJsonPipeline
from processing.utils.to_json_pipeline import ToJsonPipeline


def get_sentiment_analysis_pipeline(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(QueryParamsToFetchersPipeline('query_params_mapping', checkpointed=True)) \
        .link(FetchersToStatuses('fetch_data', checkpointed=True)) \
        .link(FlattenPipeline('flatten_data')) \
        .link(PreprocessingPipeline('preprocess', checkpointed=True)) \
        .link(SentimentAnalysisPipeline('sentiment', checkpointed=True)) \
        .link(OutputPipelineStep('output_sentiment', callback))
    return input_step


def get_json_from_tweets(callback: Callable):
    input_step = InputPipelineStep()  # Input is the query params
    input_step \
        .link(QueryParamsToFetchersPipeline('query_params_mapping', checkpointed=True)) \
        .link(FetchersToStatuses('fetch_data', checkpointed=True)) \
        .link(FlattenPipeline('flatten_data')) \
        .link(StatusesToJsonPipeline('to_json')) \
        .link(OutputPipelineStep('output_raw', callback, checkpointed=True))
    return input_step
