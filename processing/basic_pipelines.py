from typing import Callable, Optional, Any, List

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


class SplitPipelineStep(PipelineStep):
    def do_work(self, input, *args, **kwargs):
        pass

    def __init__(self, input: Optional['PipelineStep'] = None, outputs: Optional[List['PipelineStep']] = None):
        super().__init__()
        self.input = input
        self.outputs = outputs

    def link(self, outputs: List['PipelineStep']):
        self.outputs = outputs
        for output in self.outputs:
            output.input = self
        return self.outputs

    def step(self, input):
        for output in self.outputs:
            output.step(input)

class ConditionalPipelineStep(PipelineStep):
    def do_work(self, input, *args, **kwargs):
        pass

    def __init__(self, input: Optional['PipelineStep'] = None, output_true: Optional['PipelineStep'] = None, output_false: Optional['PipelineStep'] = None):
        super().__init__()
        self.input = input
        self.output_true = output_true
        self.output_false = output_false

    def link(self, output_true: 'PipelineStep', output_false: 'PipelineStep'):
        self.output_true = output_true
        self.output_false = output_false
        for output in [output_true, output_false]:
            output.input = self
        return output_true, output_false

    def step(self, input):
        if input:
            self.output_true.step(input)
        else:
            self.output_false.step(input)
