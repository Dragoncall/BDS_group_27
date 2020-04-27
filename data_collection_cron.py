import json
from time import sleep

from models.result_types import ResultType
from processing import pipeline_zoo
from processing.basic_pipelines import MergePipelineStep, OutputPipelineStep
from processing.output.file_output_pipeline import FileOutputPipeline
from processing.pipeline_zoo import _targeted_sentiment_analysis_pipeline, only_class, only_readable_class
from processing.post_processing.SentimentDistributionPipeline import SentimentDistributionPipeline
from processing.utils.map_pipeline import MapPipeline
import datetime

from processing.utils.to_json_pipeline import ToJsonPipeline


def _get_sentiment_for_person_pipeline(filename:str, result_type:ResultType=None):
    input, output = _targeted_sentiment_analysis_pipeline(
        with_handle=True, with_tags=True, with_keywords=True,
        result_type=result_type
    )

    output \
        .link(MergePipelineStep()) \
        .link(MapPipeline('only_readable_class', func=only_readable_class)) \
        .link(SentimentDistributionPipeline('sentiment_distribution')) \
        .link(ToJsonPipeline('to_json'))\
        .link(FileOutputPipeline(filename))\
        .link(OutputPipelineStep('output_sentiment_distribution', lambda x: x))
    return input

def get_prominent_people():
    with open('./resources/prominent_people.json', 'r') as f:
        loaded_json = json.load(f)
        return loaded_json.keys()

# def run_pipeline(person:str, result_type:'ResultType'):
#     _get_sentiment_for_person_pipeline(
#         f'./data_trove/{person}_{str(datetime.datetime.now())}_{result_type.name}.json',
#         result_type=result_type
#     ).feed_data(person)

if __name__ == '__main__':
    people = get_prominent_people()
    for person in people:
        print(f'Fetching Person "{person}"')
        error = True
        tries = 0
        while error:
            try:
                # _get_sentiment_for_person_pipeline(
                #     f'./data_trove/{person}_{str(datetime.datetime.now())}_mixed.json',
                #     result_type=ResultType.MIXED
                # ).feed_data(person)
                _get_sentiment_for_person_pipeline(
                    f'./data_trove/{person}_{str(datetime.datetime.now())}_recent.json',
                    result_type=ResultType.RECENT
                ).feed_data(person)
                _get_sentiment_for_person_pipeline(
                    f'./data_trove/{person}_{str(datetime.datetime.now())}_popular.json',
                    result_type=ResultType.POPULAR
                ).feed_data(person)
                # sleep(60)
                error = False
            except Exception as e:
                print(f'Error occured for {person}')
                print(e)
                error = True
                sleep(10)

            tries += 1
            if tries == 2:
                print('Maximum amount of tries, breaking')
                break
