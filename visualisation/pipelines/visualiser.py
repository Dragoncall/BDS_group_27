from processing.basic_pipelines import IdentityPipelineStep


class Visualiser(IdentityPipelineStep):
    def visualise(self, input):
        raise NotImplementedError

    def do_work(self, input, *args, **kwargs):
        self.visualise(input)
        return input