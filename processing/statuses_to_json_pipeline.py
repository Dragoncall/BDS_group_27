from processing.pipeline import CheckpointedPipelineStep


class StatusesToJsonPipeline(CheckpointedPipelineStep):
    def _do_work(self, tweets, *args, **kwargs):
        return [tweet._json for tweet in tweets]
