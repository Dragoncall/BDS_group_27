import nltk
import os
import json

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from processing.pipeline import CheckpointedPipelineStep

class CountWordDistributionPipeline(CheckpointedPipelineStep):
    """Takes a list of tweets. Returns a dictionary {word : count}"""
    def _do_work(self, input, *args, **kwargs):
        counter = {}       

        for tweet in input:
            for word in tweet.split():
                if word not in counter :
                    counter[word] = 1
                else :
                    counter[word] += 1
        
        return counter

class FilterWordDistributionPipeline(CheckpointedPipelineStep):
    """Takes a dictionary {word : count}. Removes stopwords. Returns top most frequent items."""
    def _do_work(self, input, *args, **kwargs):
        counter = {word : count for word, count in sorted(input.items(), key=lambda item: item[1], reverse=True)}
        
        keys_list = list(counter)
        keys_top = keys_list[:1]

        stop_words = []

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f'{dir_path}/../../resources/stopwords.json', 'r') as f:
            json_dict = json.load(f)
            if keys_top[0] in json_dict :
                stop_words = json_dict[keys_top[0]]['associated_stopwords']
            generic_stopwords = json_dict['generic']['associated_stopwords']

        for word in generic_stopwords:
            stop_words.append(word)
        for word in list(stopwords.words('english')):
            stop_words.append(word)
        
        stemmer = SnowballStemmer("english")

        stop_words_stemmed = []
        for word in stop_words:
             stop_words_stemmed.append(stemmer.stem(word))

        counter = {word : count for word, count \
                    in sorted(counter.items(), key=lambda item: item[1], reverse=True)\
                    if word not in stop_words_stemmed}

        keys_list = list(counter)
        if len(keys_list) < 20 :
            n = len(keys_list)
        else :
            n = 20
        keys_top = keys_list[:n]

        filtered_counter = {}
        for k in keys_top:
            filtered_counter[k] = counter[k]

        return filtered_counter