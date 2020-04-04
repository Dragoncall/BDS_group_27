from typing import Callable

from processing.pipeline import InputPipelineStep, OutputPipelineStep
from processing.preprocessing_step import PreprocessingPipeline
from processing.sentiment_analysis import SentimentAnalysisPipeline
from processing.statuses_to_json_pipeline import StatusesToJsonPipeline


def get_sentiment_analysis_pipeline(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(PreprocessingPipeline()) \
        .link(SentimentAnalysisPipeline()) \
        .link(OutputPipelineStep(callback))
    return input_step


def get_temporary_sentiment_analysis_pipeline(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(PreprocessingPipeline()) \
        .link(SentimentAnalysisPipeline()) \
        .link(StatusesToJsonPipeline()) \
        .link(OutputPipelineStep(callback))
    return input_step


def get_json_from_tweets(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(StatusesToJsonPipeline()) \
        .link(OutputPipelineStep(callback))
    return input_step
