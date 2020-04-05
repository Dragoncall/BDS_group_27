from typing import Callable, List, Any

from processing.pipeline import CheckpointedPipelineStep


class MapPipeline(CheckpointedPipelineStep):
    def __init__(self, name, func:Callable, *args, **kwargs):
        super().__init__(name)
        self.func = func

    def _do_work(self, input:List[Any], *args, **kwargs):
        return map(self.func, input)
