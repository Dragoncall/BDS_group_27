"""
This file contains all endpoints.
Keep the logic in this file to a minimum to avoid cluttering!
"""

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import data_gathering
import markdown
import markdown.extensions.fenced_code

from data_gathering import FetchBuilder
from data_gathering.sample_data_gathering import get_sample_data_gathering
from processing import pipeline_zoo
from settings import get_tweepy_client

from visualisation.offline_visualisations.timeplot_graph import read_time_data_for_person

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/raw-data')
@cross_origin()
def get_raw_data():
    """
    Fetches the raw twitter data based on the query params alone.
    Does nothing with this, just returns it to the user.
    This can be used for debugging purposes or analysis, to see on which tweets results were based.
    Example request: /raw-data?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_json_from_tweets(set_result).feed_data((params, None))
    return jsonify(result)


@app.route('/sentiment-data')
@cross_origin()
def get_sentiment_data():
    """
    Fetches the twitter data based on the query params alone.
    Does sentiment analysis on the tweets and returns the calculated value to the user
    Example request: /sentiment-data?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_sentiment_analysis_pipeline(set_result).feed_data((params, None))
    return jsonify({
        'sentiment_score': result
    })


@app.route('/sentiment-distribution')
@cross_origin()
def get_sentiment_distribution():
    """
    Fetches the twitter data based on the query params alone.
    Does sentiment analysis on the tweets and returns the sentiment distribution to the user
    Example request: /sentiment-data?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_sentiment_analysis_distribution_pipeline(set_result).feed_data((params, None))
    return jsonify({
        'sentiment_distribution': result
    })

@app.route('/word-distribution')
@cross_origin()
def get_word_distribution():
    """
    Fetches the twitter data based on the query params alone.
    Returns top most frequent words.
    Example request: /word-distribution?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_word_distribution(set_result).feed_data((params, None))
    return jsonify({
        'word_distribution': result
    })

@app.route('/wordcloud')
@cross_origin()
def get_wordcloud():
    """
    Fetches the twitter data based on the query params alone.
    Returns wordcloud.
    Example request: /wordcloud?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_full_word_distribution(set_result).feed_data((params, None))
    return jsonify({
        'word_distribution': result
    })

@app.route('/most-prevalent-sentiment')
@cross_origin()
def get_most_prevalent_sentiment():
    """
    Fetches the twitter data based on the query params alone.
    Does sentiment analysis on the tweets and returns the most prevalent sentiment to the user along with the amount
    of such sentiment observations
    Example request: /most-prevalent-sentiment?query=kek&count=1
    """
    params = request.args
    result = None

    def set_result(x):
        nonlocal result  # This is ugly, ew, gotta fix this
        result = x

    pipeline_zoo.get_sentiment_analysis_most_prevalent_pipeline(set_result).feed_data((params, None))
    return jsonify({
        'sentiment_distribution': result
    })

@app.route('/sentiment-history')
@cross_origin()
def get_sentiment_history():
    """
    Does sentiment analysis on the stored tweets of a promiment figure
    Returns the history of sentiment distribution to the user
    Example request: /sentiment-history?figure=kek&result_type=recent
    """
    params = request.args
    result = {}

    handle = params['figure']
    result_type = params['result_type']

    df = read_time_data_for_person(handle, result_type)

    for index, row in df.iterrows():
        result[index] = dict(row)

    return jsonify({
        'sentiment_distribution': result
    })

@app.route('/')
def index():
    with open("PROJECT.md", "r") as project_file:
        md_template_string = markdown.markdown(
            project_file.read(), extensions=["fenced_code"]
        )
    return md_template_string


if __name__ == '__main__':
    app.run()
