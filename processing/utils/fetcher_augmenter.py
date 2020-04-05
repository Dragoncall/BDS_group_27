from typing import List, Tuple, Dict, Any

from data_gathering import FetchBuilder
from processing.pipeline import CheckpointedPipelineStep


class FetcherAugmenter(CheckpointedPipelineStep):
    def __init__(self, name, update_dict: Dict[str, Any], *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.update_dict = update_dict


    def _do_work(self, fetches:List[FetchBuilder], *args, **kwargs):
        for fetch in fetches:
            for k,v in self.update_dict.items():
                fetch._set_attr(k, v)
        return fetches
