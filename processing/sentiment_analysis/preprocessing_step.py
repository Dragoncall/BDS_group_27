import re
import string
import nltk
import emoji

from nltk.stem.snowball import SnowballStemmer
from tokenizer import tokenizer

from processing.pipeline import CheckpointedPipelineStep

class PreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):
        # include all preprocessing steps in here ?
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
        punct += '’'
        punct += '“”'
        punct += '«»'

        punct = re.sub(' ', '', punct)  # keep spaces
        punct = re.sub('#', '', punct)  # keep hashtags
        punct = re.sub('@', '', punct)  # keep mentions
        #punct = re.sub('\'', '', punct) # keep single quotes (in order to retain I'm, isn't, etc.)

        input = "".join([char for char in input if char not in punct])

        return input

class RemoveMentionsPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        mention_regex = r'@\S+'
        input = re.sub(mention_regex, '', input)

        return input

class RemoveHashTagsPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        hashtag_regex = r'#\S+'
        input = re.sub(hashtag_regex, '', input)

        return input

class RemoveWhiteSpacePreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        space_regex = r'\s+'
        input = re.sub(space_regex, ' ', input)
        input = input.strip()
        return input

class ConvertEmojisPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input:str, *args, **kwargs):
        return emoji.demojize(input)

class StemPreprocessingPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):
        T = tokenizer.TweetTokenizer(regularize=True)
        input = T.tokenize(input)
        stemmer = SnowballStemmer("english")
        
        tweet = ''
        for word in input:
            word = stemmer.stem(word)
            tweet += word+' '

        return tweet