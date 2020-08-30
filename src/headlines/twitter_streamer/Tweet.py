from typing import List
from textblob import TextBlob


class Tweet:
    """ Class to hold tweet objects"""
    def __init__(self, text: str, retweets: int, hashtags: List[str]):
        self.text = text
        self.retweets = retweets
        self.hashtags = set(hashtags)

    def positivity(self) -> float:
        """ Returns how positive a tweet is based on the TextBlob Library"""
        return TextBlob(self.text).polarity

    def __eq__(self, other_tweet):
        """ This will allow us to avoid searching an indentical tweet if it is obtained twice somehow"""
        return other_tweet.hashtags == self.hashtags and self.text == self.text




