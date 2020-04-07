from typing import Dict, List, Tuple

from data_gathering import query_param_mapping, FetchBuilder
from processing.pipeline import CheckpointedPipelineStep
from settings import get_tweepy_client


class FetchersToStatuses(CheckpointedPipelineStep):
    def _do_work(self, input:List[FetchBuilder], *args, **kwargs):
        api = get_tweepy_client()
        return [fetcher.run(api) for fetcher in input]


def statuses_fetch(query_params: Dict[str, str]):
    api = get_tweepy_client()
    return [tweet for tweet in query_param_mapping.query_params_compiler(query_params, FetchBuilder()).run(api)]
