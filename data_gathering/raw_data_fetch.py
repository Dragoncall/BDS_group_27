from typing import Dict

from data_gathering import query_param_mapping
from data_gathering.fetch_builder import FetchBuilder
from settings import get_tweepy_client


def raw_data_fetch(query_params: Dict[str, str]):
    api = get_tweepy_client()
    return [tweet._json for tweet in query_param_mapping.query_params_compiler(query_params, FetchBuilder()).run(api)]