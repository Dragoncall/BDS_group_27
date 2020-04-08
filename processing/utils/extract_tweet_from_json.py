from processing.pipeline import CheckpointedPipelineStep

class ExtractTweetFromJson(CheckpointedPipelineStep):
    """Extracts Tweet string from JSON representation"""
    def _do_work(self, tweets, *args, **kwargs):
        return [tweet['full_text'] for tweet in tweets]