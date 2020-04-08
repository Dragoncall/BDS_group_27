import tweepy

from models.geocode import GeoCode
from models.result_types import ResultType


class FetchBuilder:
    """
    Class that builds a search tweepy request as defined here:
    http://docs.tweepy.org/en/latest/api.html#help-methods

    This class uses the builder pattern to allow for easy compilation of these query parameters
    """
    def __init__(self):
        self.geocode = None
        self.lang = None
        self.query = None
        self.result_type = None
        self.count = 1
        self.until = None
        self.since_id = None
        self.max_id = None
        self.tweet_mode = 'extended'
        self.filter_retweets = None

    def _set_attr(self, key, value):
        self.__setattr__(key, value)
        return self

    def set_geocode(self, val:'GeoCode'):
         return self._set_attr('geocode', val)

    def set_lang(self, val:str):
         return self._set_attr('lang', val)

    def set_query(self, val:str):
         return self._set_attr('q', val)

    def set_result_type(self, val:'ResultType'):
         return self._set_attr('result_type', val)

    def set_count(self, val:int):
         return self._set_attr('count', val)

    def set_until(self, val:str):
         return self._set_attr('until', val)

    def set_since_id(self, val:int):
         return self._set_attr('since_id', val)

    def set_max_id(self, val:int):
         return self._set_attr('max_id', val)

    def set_tweet_mode(self, val:str):
         return self._set_attr('tweet_mode', val)

    def set_filter_retweets(self, val:str):
         return self._set_attr('filter_retweets', val)

    def compile_query_params(self):
        query_dict = self.__dict__
        query_dict.pop('count', None)

        if query_dict['filter_retweets'] == 'True':
             query_dict['q'] += '-filter:retweets'

        query_dict.pop('filter_retweets', None)

        return query_dict

    def build(self):
        count = self.count
        return lambda api: tweepy.Cursor(api.search, **self.compile_query_params()).items(count)

    def run(self, api: tweepy.API):
        list_statuses = []
        for status in self.build()(api):
             list_statuses.append(status)
        return list_statuses


if __name__ == '__main__':
    """Sample usage of the FetchBuilder"""

    from settings import get_tweepy_client

    builder = FetchBuilder().set_count(100).set_query('test')
    api = get_tweepy_client()
    print(builder.run(api))