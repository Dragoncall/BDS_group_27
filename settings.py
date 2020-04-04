import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_key")
API_SECRET = os.getenv("API_secret_key")

ACCESS_KEY = os.getenv("Access_token")
ACCESS_SECRET = os.getenv("Access_token_secret")

TWEEPY_CLIENT = None


def get_tweepy_client():
    global TWEEPY_CLIENT

    if TWEEPY_CLIENT is None:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        TWEEPY_CLIENT = tweepy.API(auth)
    return TWEEPY_CLIENT
