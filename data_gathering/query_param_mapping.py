from typing import Union, List, Dict, Tuple

from data_gathering.fetch_builder import FetchBuilder
from processing.pipeline import CheckpointedPipelineStep

query_param_map = {
    'query': lambda x, builder: builder.set_query((builder.query or '') + ' ' + x),
    'geocode': lambda x, builder: builder,  # TODO: map our geocode string to our GeoCode object
    'lang': lambda x, builder: builder.set_lang(x),
    'result_type': lambda x, builder: builder,  # TODO: map our geocode string to our ResultType object
    'count': lambda x, builder: builder.set_count(int(x)),
    'until': lambda x, builder: builder.set_until(x),
    'since_id': lambda x, builder: builder.set_since_id(int(x)),
    'max_id': lambda x, builder: builder.set_max_id(int(x))
}


class QueryParamsToFetchersPipeline(CheckpointedPipelineStep):
    def _do_work(self, input: Tuple[Dict[str, str], List[FetchBuilder]], *args, **kwargs):
        query_params, fetchers = input
        if fetchers is None:
            fetchers = [FetchBuilder()]
        return query_params_compiler(query_params, fetchers)


def query_params_compiler(query_params: Dict[str, str], fetchers: Union[FetchBuilder, List[FetchBuilder]]):
    was_list = True
    if not isinstance(fetchers, list):
        was_list = False
        fetchers = [fetchers]

    # Fill in all fetchers with the extra query params
    for fetcher in fetchers:
        for k, v in query_params.items():
            query_param_map[k](v, fetcher)

    return fetchers if was_list else fetchers[0]
