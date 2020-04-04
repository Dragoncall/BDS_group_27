from processing.pipeline import PipelineStep


class PreprocessingPipeline(PipelineStep):
    def do_work(self, input, *args, **kwargs):
        return input  # TODO: implement this
