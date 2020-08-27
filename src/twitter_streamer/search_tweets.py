import tweepy
from typing import Set
from typing import List
from twitter_streamer import API_keys
from twitter_streamer import Tweet
from twitter_streamer.twitter_stream import TwitterListener


def get_tweets(tracked_words: List[str], time_limit = 300) -> List[Tweet]:
    twitter_api = get_api()
    listener = TwitterListener(time_limit)
    stream = tweepy.Stream(auth=twitter_api.auth, listener=listener,
                        tweet_mode="extended")
    stream.filter(track=tracked_words)
    return stream.tweets


def get_api():
    api_key = API_keys.get_api_key()
    api_secret_key = API_keys.get_secret_key()
    access_token =  API_keys.get_access_token()
    secret_access_token = API_keys.get_secret_access_token()
    authentication = tweepy.OAuthHandler(api_key, api_secret_key)
    authentication.set_access_token(access_token, secret_access_token)
    return tweepy.API(authentication) # twitter API

