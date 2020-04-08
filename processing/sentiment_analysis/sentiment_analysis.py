import os
import pickle

import tensorflow as tf
from keras.initializers import glorot_uniform
from keras.preprocessing.sequence import pad_sequences
from keras.utils import CustomObjectScope

from processing.pipeline import CheckpointedPipelineStep


class SentimentAnalysisPipeline(CheckpointedPipelineStep):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # load model
        # colab version : 2.3.0-tf
        modelpath = dir_path + '/../../resources/lstm_model.h5'
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            self.model = tf.keras.models.load_model(modelpath)

        # load tokenizer fitted on traning data
        with open(f'{dir_path}/../../resources/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)


    def _do_work(self, input, *args, **kwargs):
        max_length = 29

        X = self.tokenizer.texts_to_sequences([input])
        X = pad_sequences(X, maxlen=max_length)

        predictions = self.model.predict_classes(X)
        probabilities = self.model.predict_proba(X)

        return int(predictions[0]), [float(x) for x in probabilities[0].tolist()]
