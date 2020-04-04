"""
This file contains all endpoints.
Keep the logic in this file to a minimum to avoid cluttering!
"""

from flask import Flask, jsonify

from data_gathering.sample_data_gathering import get_sample_data_gathering
from settings import get_tweepy_client

app = Flask(__name__)

@app.route('/test')
def test_get_tweet():
    return jsonify(get_sample_data_gathering('twitter'))

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
