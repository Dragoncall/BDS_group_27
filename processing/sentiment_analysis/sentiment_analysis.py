import os
import pickle

from processing.pipeline import CheckpointedPipelineStep


class SentimentAnalysisPipeline(CheckpointedPipelineStep):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # load model
        with open(f'{dir_path}/../../resources/model_log_reg.sav', 'rb') as handle:
            self.model = pickle.load(handle)

        # load tokenizer fitted on traning data
        with open(f'{dir_path}/../../resources/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)


    def _do_work(self, input, *args, **kwargs):
        X = self.tokenizer.transform([input])

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        return int(predictions[0]), [float(x) for x in probabilities[0].tolist()]
