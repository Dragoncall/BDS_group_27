from processing.pipeline import CheckpointedPipelineStep

class ExtractTweetFromJson(CheckpointedPipelineStep):
    """Extracts Tweet string from JSON representation"""
    def _do_work(self, tweets, *args, **kwargs):
        return [
            tweet['full_text']
            if 'full_text' in tweet
            else tweet['text']
            for tweet in tweets
        ]