from processing.pipeline import PipelineStep


class StatusesToJsonPipeline(PipelineStep):
    def do_work(self, tweets, *args, **kwargs):
        return [tweet._json for tweet in tweets]
