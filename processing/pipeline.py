from typing import Any, Optional, Callable


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
        self.step(data)


class OutputPipelineStep(PipelineStep):
    """
    A pipeline step that is used as the last step in a pipeline. The data is then passed to a final callback.
    """

    def __init__(self, callback: Callable, input: Optional['PipelineStep'] = None):
        super().__init__(input, None)
        self.callback = callback

    def step(self, input):
        self.callback(input)


if __name__ == '__main__':
    """A small example of the usage of pipeline steps."""
    input_step = InputPipelineStep()
    input_step.link(IdentityPipelineStep()).link(OutputPipelineStep(lambda x: print(x)))
    input_step.feed_data('Well hello there!')
