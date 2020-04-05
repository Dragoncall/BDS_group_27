from processing.pipeline import CheckpointedPipelineStep


class PreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):
        return input  # TODO: implement this
