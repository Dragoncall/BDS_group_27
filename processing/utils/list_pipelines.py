from collections import Counter
from typing import Callable

from processing.pipeline import PipelineStep


class MaxPipeline(PipelineStep):
    def __init__(self, key: Callable = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key

    def do_work(self, input, *args, **kwargs):
        return max(input, key=self.key)


class MinPipeline(PipelineStep):
    def __init__(self, key: Callable = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key

    def do_work(self, input, *args, **kwargs):
        return min(input, key=self.key)


class CountPipeline(PipelineStep):
    def do_work(self, input, *args, **kwargs):
        return Counter(input).most_common()


class GetAtIndexPipeline(PipelineStep):
    def __init__(self, index: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index

    def do_work(self, input, *args, **kwargs):
        return input[self.index]
