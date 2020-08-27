import functools
from typing import List, Dict
from headlines import advanced_headline
from twitter_streamer import search_tweets
from twitter_streamer import Tweet

class Cluster:
    """ Will be used to store information about extracted cluster"""
    def __init__(self, id_articles: Dict[int, advanced_headline], central_features: List[str]):
        self.ids id_articles
        self.central_features = central_features
        self.tweets: List[Tweet] = []
        self.avg_positivity: float = None # floats in python are very precise

    def get_tweets(self):
        self.tweets = search_tweets.get_tweets(self.central_features)
        self.avg_positivity = functools.reduce(lambda a,b : a.positivity + b.positivity, self.tweets) / len(self.tweets)

    def create_insert(self):
        return f"INSERT INTO Clusters(keywords, numTweets, avg_rating) Values({self.keywords.join(' ')}, {len(self.tweets)}, {self.avg_positivity}"



