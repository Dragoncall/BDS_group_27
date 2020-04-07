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
        self.count = None
        self.until = None
        self.since_id = None
        self.max_id = None
        self.tweet_mode = 'extended'

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

    def compile_query_params(self):
        return self.__dict__

    def build(self):
        return lambda api: api.search(**self.compile_query_params())

    def run(self, api: tweepy.API):
        return self.build()(api)


if __name__ == '__main__':
    """Sample usage of the FetchBuilder"""

    from settings import get_tweepy_client

    builder = FetchBuilder().set_count(100).set_query('test')
    api = get_tweepy_client()
    print(builder.run(api))