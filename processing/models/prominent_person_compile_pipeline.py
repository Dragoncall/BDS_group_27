from typing import Tuple

from models.prominent_person import ProminentUser
from processing.pipeline import CheckpointedPipelineStep


class ProminentPersonCompilePipeline(CheckpointedPipelineStep):
    def __init__(self, name, with_handle=False, with_tags=False, with_keywords=False, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.with_handle = with_handle
        self.with_tags = with_tags
        self.with_keywords = with_keywords

    def _do_work(self, input:str, *args, **kwargs):
        # Input is the handle of a person
        user = None
        try:
            user = ProminentUser.from_resources(input)
        except KeyError:
            user = ProminentUser(input, None, [], [])

        return user.compile_fetchers(
            with_handle=self.with_handle,
            with_keywords=self.with_keywords,
            with_tags=self.with_tags
        )

class ProminentPersonCompileOnArgsPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:Tuple[str, bool, bool, bool], *args, **kwargs):
        # Input is the handle of a person | with_handle | with_tags | with_keywords
        handle, with_handle, with_tags, with_keywords = input
        user = None
        try:
            user = ProminentUser.from_resources(input)
        except KeyError:
            user = ProminentUser(handle, None, [], [])

        return user.compile_fetchers(
            with_handle=with_handle,
            with_keywords=with_keywords,
            with_tags=with_tags
        )
