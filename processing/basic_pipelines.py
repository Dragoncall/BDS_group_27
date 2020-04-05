from typing import Callable, Optional, Any

from processing.pipeline import PipelineStep, CheckpointedPipelineStep


class IdentityPipelineStep(PipelineStep):
    """A pipeline step that gives its input to the next step"""

    def do_work(self, input, *args, **kwargs):
        return input


class InputPipelineStep(IdentityPipelineStep):
    """
    A pipeline step that takes input data. Mostly used as the first step in a pipeline.
    This step kicks off the pipeline by feeding data to it by using the feed_data function.
    """

    def __init__(self, output: Optional['PipelineStep'] = None):
        super().__init__(None, output)

    def feed_data(self, data: Any):
        """Feed data into this pipeline"""
        self.step(data)

    def _find_final_checkpoint_last_run(self):
        current_step = self
        last_checkpoint = None
        while current_step.output is not None:
            current_step = current_step.output
            if isinstance(current_step, CheckpointedPipelineStep) and current_step.last_checkpoint is not None:
                last_checkpoint = current_step
        return last_checkpoint

    def _run_step_for_key(self, last_checkpoint, key):
        print(f'Running for {last_checkpoint.name} with input hash {last_checkpoint.last_checkpoint}')
        result = last_checkpoint.get_checkpoint(key)
        last_checkpoint.step(None, result=result)

    def continue_last_checkpoint(self):
        """Continue the pipeline from the last ran checkpointed step. The same input will be used."""
        last_checkpoint = self._find_final_checkpoint_last_run()
        if last_checkpoint is None:
            raise ValueError('Cannot continue the last checkpoint when no runs have been done!')
        self._run_step_for_key(last_checkpoint, last_checkpoint.last_checkpoint)


    def continue_last_checkpoint_for_hash(self, input_hash):
        current_step = self
        last_checkpoint = None
        while current_step.output is not None:
            current_step = current_step.output
            if isinstance(current_step, CheckpointedPipelineStep) and current_step.has_checkpoint(input_hash):
                last_checkpoint = current_step
        if last_checkpoint is None:
            raise ValueError(f'No checkpoint for key {input_hash}')
        self._run_step_for_key(last_checkpoint, input_hash)



class OutputPipelineStep(CheckpointedPipelineStep):
    """
    A pipeline step that is used as the last step in a pipeline. The data is then passed to a final callback.
    """

    def __init__(self, name, callback: Callable, input: Optional['PipelineStep'] = None, checkpointed=False):
        super().__init__(name, input=input, output=None, checkpointed=checkpointed)
        self.callback = callback

    def _do_work(self, input, *args, **kwargs):
        return input

    def step(self, input, result=None):
        """Final step in the pipeline. Calls a callback with the result"""
        self.callback(result or self.do_work(input))

