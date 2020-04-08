import random
import pickle
import os
import tensorflow as tf

from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform

from processing.pipeline import CheckpointedPipelineStep


class SentimentAnalysisPipeline(CheckpointedPipelineStep):
    def _do_work(self, input, *args, **kwargs):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # load model
        # colab version : 2.3.0-tf
        modelpath = dir_path + '/../../resources/lstm_model.h5'
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            model = tf.keras.models.load_model(modelpath)

        # load tokenizer fitted on traning data
        with open(f'{dir_path}/../../resources/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        max_length = 29

        X = tokenizer.texts_to_sequences([input])
        X = pad_sequences(X, maxlen=max_length)

        predictions = model.predict_classes(X)

        return predictions
