from settings import get_tweepy_client


def get_sample_data_gathering(username):
    api = get_tweepy_client()
    user = api.get_user(username)
    return {
        'name': user.screen_name,
        'followers': user.followers_count
    }