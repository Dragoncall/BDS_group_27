from typing import Callable, List, Any

from processing.pipeline import CheckpointedPipelineStep


class MapPipeline(CheckpointedPipelineStep):
    """Maps a list of input values using a predefined func"""
    def __init__(self, name, func:Callable, *args, **kwargs):
        super().__init__(name)
        self.func = func

    def _do_work(self, input:List[Any], *args, **kwargs):
        return list(map(self.func, input))
