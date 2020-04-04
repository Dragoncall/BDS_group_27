from typing import List, Dict, Optional

import tweepy

from data_gathering.fetch_builder import FetchBuilder
from models.twitter_user import TwitterUser


class ProminentUser(TwitterUser):
    def __init__(self, handle: str, api: Optional[tweepy.API], associated_tags: List[str],
                 associated_keywords: List[str]):

        super().__init__(handle, api)
        self.associated_tags = associated_tags
        self.associated_keywords = associated_keywords

    def _create_tag_fetcher(self, tag):
        return FetchBuilder().set_query(tag)

    def _create_keyword_fetcher(self, keyword):
        return FetchBuilder().set_query(keyword)

    def _create_handle_fetcher(self, handle):
        return FetchBuilder().set_query(f'@{handle}')

    def compile_fetchers(self, with_tags=True, with_keywords=True, with_handle=True):
        fetchers = []
        if with_tags:
            fetchers += [self._create_tag_fetcher(tag) for tag in self.associated_tags]
        if with_keywords:
            fetchers += [self._create_keyword_fetcher(keyword) for keyword in self.associated_keywords]
        if with_handle:
            fetchers += [self._create_handle_fetcher(self.handle)]
        return fetchers

# TODO: we need to add some prominent people with their handles, their keywords and their tags here
# Or find some way to automatically find these tags & keywords
# The fallback plan should always to check for mentions using their handle