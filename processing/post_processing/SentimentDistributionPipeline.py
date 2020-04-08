from processing.pipeline import CheckpointedPipelineStep


class SentimentDistributionPipeline(CheckpointedPipelineStep):
    """Takes a list of classes. Returns the distribution"""
    def _do_work(self, input, *args, **kwargs):
        unique_sentiments = {sentiment for sentiment in input}
        return {sentiment: input.count(sentiment)/len(input) for sentiment in unique_sentiments}
