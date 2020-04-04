from typing import Dict

from data_gathering import query_param_mapping, FetchBuilder
from settings import get_tweepy_client


def statuses_fetch(query_params: Dict[str, str]):
    api = get_tweepy_client()
    return [tweet for tweet in query_param_mapping.query_params_compiler(query_params, FetchBuilder()).run(api)]
