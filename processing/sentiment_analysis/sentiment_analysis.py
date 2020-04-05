import random

from processing.pipeline import CheckpointedPipelineStep


class SentimentAnalysisPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):
        return random.random()  # TODO: implement this
