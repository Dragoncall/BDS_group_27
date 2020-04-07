import re
import string

from processing.pipeline import CheckpointedPipelineStep

class PreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):
        # include all preprocessing steps below here ?
        return input  # TODO: implement this

class LowerCasePreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        return input.lower()

class RemoveUrlPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        url_regex = r'https?://\S+'
        input = re.sub(url_regex, '', input)
        return input

class RemoveNumberPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        number_regex = r'\d+'
        input = re.sub(number_regex, '', input)
        return input

class RemovePunctuationPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        punct = string.punctuation

        punct = re.sub(' ', '', punct)  # keep spaces
        punct = re.sub('#', '', punct)  # keep hashtags
        punct = re.sub('@', '', punct)  # keep mentions
        punct = re.sub('\'', '', punct) # keep single quotes (in order to retain I'm, isn't, etc.)

        input = "".join([char for char in input if char not in punct])

        return input

class RemoveWhiteSpacePreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        space_regex = r'\s+'
        input = re.sub(space_regex, ' ', input)
        input = input.strip()
        return input
