from processing.pipeline import PipelineStep


class FileOutputPipeline(PipelineStep):
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename

    def do_work(self, input, *args, **kwargs):
        if self.filename:
            with open(self.filename, 'w+') as f:
                f.write(input)
        return input
