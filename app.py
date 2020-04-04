"""
This file contains all endpoints.
Keep the logic in this file to a minimum to avoid cluttering!
"""

from flask import Flask, jsonify, request
import data_gathering
import markdown
import markdown.extensions.fenced_code

from data_gathering.sample_data_gathering import get_sample_data_gathering
from processing import pipeline_zoo
from settings import get_tweepy_client

app = Flask(__name__)


@app.route('/raw-data')
def get_raw_data():
    """
    Fetches the raw twitter data based on the query params alone.
    Does nothing with this, just returns it to the user.
    This can be used for debugging purposes or analysis, to see on which tweets results were based.
    Example request: /raw-data?query=kek&count=1
    """
    params = request.args
    tweets = data_gathering.statuses_fetch(params)
    result = None

    def set_result(x):
        nonlocal result # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_json_from_tweets(set_result).feed_data(tweets)
    return jsonify(result)


@app.route('/sentiment-data')
def get_pipelined_data():
    """
    Fetches the raw twitter data based on the query params alone.
    Does nothing with this, just returns it to the user.
    This can be used for debugging purposes or analysis, to see on which tweets results were based.
    Example request: /raw-data?query=kek&count=1
    """
    params = request.args
    tweets = data_gathering.statuses_fetch(params)
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_temporary_sentiment_analysis_pipeline(set_result).feed_data(tweets)
    return jsonify(result)

@app.route('/')
def index():
    with open("PROJECT.md", "r") as project_file:
        md_template_string = markdown.markdown(
            project_file.read(), extensions=["fenced_code"]
        )
    return md_template_string


if __name__ == '__main__':
    app.run()
