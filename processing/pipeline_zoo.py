from typing import Callable

from processing.basic_pipelines import InputPipelineStep, OutputPipelineStep
from processing.sentiment_analysis.preprocessing_step import PreprocessingPipeline
from processing.sentiment_analysis.sentiment_analysis import SentimentAnalysisPipeline
from processing.core.statuses_to_json_pipeline import StatusesToJsonPipeline


def get_sentiment_analysis_pipeline(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(PreprocessingPipeline('preprocess')) \
        .link(SentimentAnalysisPipeline('sentiment')) \
        .link(OutputPipelineStep('output', callback))
    return input_step


def get_temporary_sentiment_analysis_pipeline(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(PreprocessingPipeline('preprocess')) \
        .link(SentimentAnalysisPipeline('sentiment')) \
        .link(StatusesToJsonPipeline('to_json')) \
        .link(OutputPipelineStep('output', callback))
    return input_step


def get_json_from_tweets(callback: Callable):
    input_step = InputPipelineStep()
    input_step \
        .link(StatusesToJsonPipeline('to_json')) \
        .link(OutputPipelineStep('output', callback))
    return input_step
