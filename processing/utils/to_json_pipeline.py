import json
from typing import Callable, List, Any

from processing.pipeline import CheckpointedPipelineStep


class ToJsonPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:Any, *args, **kwargs):
        return json.dumps(input)
