from typing import Optional

import tweepy as tweepy

class TwitterUser(object):
    def __init__(self, handle: str, api: Optional[tweepy.API]):
        self.handle = handle
        self._api = api

    @property
    def api(self):
        if self._api is not None:
            return self._api
        raise ValueError(f'Cannot use the API when its value is: {repr(self._api)}')

    @property
    def user(self):
        return self.api.get_user(self.handle)
