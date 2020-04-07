from typing import Callable, List, Any

from processing.pipeline import CheckpointedPipelineStep


class FilterPipeline(CheckpointedPipelineStep):
    """Filters a list of input values using a predefined func"""
    def __init__(self, name, func:Callable, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.func = func

    def _do_work(self, input:List[Any], *args, **kwargs):
        return filter(self.func, input)
