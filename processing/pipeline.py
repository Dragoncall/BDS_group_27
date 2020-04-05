import pickle
from pathlib import Path
from typing import Any, Optional, Callable

checkpoint_dir = Path(f'./checkpoints')
if not checkpoint_dir.is_dir():
    checkpoint_dir.mkdir()


class PipelineStep:
    """Class that depicts a step in the processing pipeline"""

    def __init__(self, input: Optional['PipelineStep'] = None, output: Optional['PipelineStep'] = None):
        self.input = input
        self.output = output

    def do_work(self, input, *args, **kwargs):
        raise NotImplementedError

    def step(self, input):
        self.output.step(self.do_work(input))

    def link(self, output: 'PipelineStep'):
        self.output = output
        output.input = self
        return self.output


class CheckpointedPipelineStep(PipelineStep):
    """
    Checkpointed pipeline step. Allows for rapid development due to caching the
    result of a given input on the input's hash.
    Each of these pipelines needs a name to know to which file to write the checkpoints.
    Checkpointing can be enabled by setting checkpointed to True.
    """

    def __init__(self, name, input: Optional['PipelineStep'] = None, output: Optional['PipelineStep'] = None,
                 checkpointed=False):
        super().__init__(input, output)
        self.checkpointed = checkpointed
        self.name = name

        self.checkpoint_dict = {}
        if self.has_checkpoint_file():
            self.reload()

        self.last_checkpoint = None

    @property
    def checkpoint_name(self):
        return Path(f'./checkpoints/checkpoint_{self.name}.txt')

    def set_checkpoint(self, key, result):
        """Set cache value for input hash"""
        self.checkpoint_dict[key] = result
        with self.checkpoint_name.open('wb+') as f:
            pickle.dump(self.checkpoint_dict, f)

    def get_checkpoint(self, key):
        """Get cache value for input hash"""
        return self.checkpoint_dict[key]

    def has_checkpoint_file(self):
        """Has checkpoint file"""
        return self.checkpoint_name.exists()

    def has_checkpoint(self, key):
        """Has value for given input hash"""
        return key in self.checkpoint_dict

    def reload(self):
        """Reload the cache file"""
        with self.checkpoint_name.open('rb') as f:
            try:
                self.checkpoint_dict = pickle.load(f)
            except EOFError:
                self.checkpoint_dict = {}

    def _do_work(self, input, *args, **kwargs):
        raise NotImplementedError

    def do_work(self, input, *args, **kwargs):
        key = pickle.dumps(input)

        # Do we have the value in cache? Yes -> return this value
        if self.checkpointed and self.has_checkpoint(key):
            return self.get_checkpoint(key)

        # Do we have the value in cache? No -> calculate the value and store it on the input hash
        result = self._do_work(input, *args, **kwargs)
        if self.checkpointed:
            self.last_checkpoint = key
            self.set_checkpoint(key, result)
        return result

    def step(self, input, result=None):
        if result is None:
            super(CheckpointedPipelineStep, self).step(input)
        return result


if __name__ == '__main__':
    from processing.basic_pipelines import InputPipelineStep, IdentityPipelineStep, OutputPipelineStep

    """A small example of the usage of pipeline steps."""
    input_step = InputPipelineStep()
    input_step.link(IdentityPipelineStep()).link(OutputPipelineStep('output', lambda x: print(x)))
    input_step.feed_data('Well hello there!')

    """Example with checkpointing"""

    input_step = InputPipelineStep()
    input_step\
        .link(IdentityPipelineStep())\
        .link(OutputPipelineStep('output', lambda x: print(x), checkpointed=True))
    input_step.feed_data('Well hello there!')

    input_step.continue_last_checkpoint()  # Uses the last stored checkpoint
    input_step.continue_last_checkpoint_for_hash(pickle.dumps('Well hello there!'))  # Uses the hash as checkpoint key
    input_step.output.output.step('Well hello there!')  # Runs the last step directly using certain input 
