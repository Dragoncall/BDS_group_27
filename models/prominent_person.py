import json
import os
from typing import List, Optional

import tweepy

from data_gathering.fetch_builder import FetchBuilder
from models.twitter_user import TwitterUser


class ProminentUser(TwitterUser):
    def __init__(self, handle: str, api: Optional[tweepy.API], associated_tags: List[str],
                 associated_keywords: List[str]):

        super().__init__(handle, api)
        self.associated_tags = associated_tags
        self.associated_keywords = associated_keywords

    @staticmethod
    def from_resources(handle):
        """
        Searches the handle in the 'prominent_people.json' file and inits the class with
        the added keywords and tags.
        Raises a ValueError is the handle is not found in the resource.
        """

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f'{dir_path}/../resources/prominent_people.json', 'r') as f:
            json_dict = json.load(f)
            person = json_dict[handle]
            return ProminentUser(
                handle, api=None,
                associated_tags=person['associated_tags'],
                associated_keywords=person['associated_keywords']
            )


    def _create_tag_fetcher(self, tag):
        return FetchBuilder().set_query(tag)

    def _create_keyword_fetcher(self, keyword):
        return FetchBuilder().set_query(keyword)

    def _create_handle_fetcher(self, handle):
        return FetchBuilder().set_query(f'@{handle}')

    def compile_fetchers(self, with_tags=True, with_keywords=True, with_handle=True) -> List[FetchBuilder]:
        fetchers = []
        if with_tags:
            fetchers += [self._create_tag_fetcher(tag) for tag in self.associated_tags]
        if with_keywords:
            fetchers += [self._create_keyword_fetcher(keyword) for keyword in self.associated_keywords]
        if with_handle:
            fetchers += [self._create_handle_fetcher(self.handle)]
        return fetchers
