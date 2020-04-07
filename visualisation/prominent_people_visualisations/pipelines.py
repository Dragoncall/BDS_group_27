from typing import Union, List
from processing.basic_pipelines import InputPipelineStep, SpreadPipelineStep, PrintPipelineStep
from processing.models.prominent_person_compile_pipeline import ProminentPersonCompileOnArgsPipeline


def default_prominent_people_pipeline():
    input_step = InputPipelineStep()
    input_step.link(SpreadPipelineStep()) \
        .link(PrintPipelineStep()) \
        .link(ProminentPersonCompileOnArgsPipeline('prominent_person'))
    return input_step


def run_prominent_people_pipeline(pipeline:InputPipelineStep, handle_or_list: Union[str, List[str]], with_tags=True, with_keywords=True, with_handle=True):
    if isinstance(handle_or_list, str):
        pipeline.feed_data([(handle_or_list, with_handle, with_tags, with_keywords)])
    else:
        pipeline.feed_data([
            (handle, with_handle, with_tags, with_keywords)
            for handle in handle_or_list
        ])