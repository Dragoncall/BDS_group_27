from processing.pipeline import CheckpointedPipelineStep


class StatusesToJsonPipeline(CheckpointedPipelineStep):
    """Maps a Status object to its JSON representation"""
    def _do_work(self, tweets, *args, **kwargs):
        return [tweet._json for tweet in tweets]
