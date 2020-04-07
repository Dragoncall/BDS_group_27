import json
from typing import Callable, List, Any

from processing.pipeline import CheckpointedPipelineStep


class ToJsonPipeline(CheckpointedPipelineStep):
    """Maps an object to its JSON representation"""
    def _do_work(self, input:Any, *args, **kwargs):
        return json.dumps(input)
