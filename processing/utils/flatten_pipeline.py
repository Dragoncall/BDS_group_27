from typing import List, Any

from processing.pipeline import CheckpointedPipelineStep


class FlattenPipeline(CheckpointedPipelineStep):
    """Flattens a list of lists into a single flat list"""
    def _do_work(self, input:List[List[Any]], *args, **kwargs):
        return [y for x in input for y in x]

