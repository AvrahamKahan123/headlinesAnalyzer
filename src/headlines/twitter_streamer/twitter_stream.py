import tweepy, time
from typing import List
from headlines.twitter_streamer import Tweet
from headlines.psql_util import execute_multiple_inserts
from headlines.twitter_streamer import API_keys


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



class TwitterListener(tweepy.StreamListener):
    """ Stream establishes single persistent connection to stream realtime tweets"""
    def __init__(self, time_limit=200):
        super(TwitterListener, self).__init__()
        self.start_time = time.time()
        self.limit = time_limit
        self.tweets: List[Tweet] = []

    def add_tweet(self, new_tweet: Tweet):
        self.tweets.append(new_tweet)

    def on_status(self, status):
        if not hasattr(status, "retweeted_status") and status.lang == "en":
            tweet_obj = self.construct_tweet(status)
            self.add_tweet(tweet_obj)
        return self.check_time()

    def construct_tweet(self, current_tweet):
        if current_tweet.truncated:  # tweet is > 140 characters
            tweet_text = current_tweet.extended_tweet['full_text']
            hashtags = [tag['text'] for tag in current_tweet.extended_tweet['entities']['hashtags']]
        else:
            tweet_text = current_tweet.text
            hashtags = [tag['text'] for tag in current_tweet.entities['hashtags']]
        current_tweet.retweet_count
        return Tweet(tweet_text, current_tweet.retweet_count, hashtags)

    def check_time(self):
        if (time.time() - self.start_time) > self.limit:
            self.write_to_db()
            return False
        return True # maybe should be changed to None / removed

    def write_to_db(self) -> None:
        """ Writes tweets to DBs since multiple writes at once with one commit is faster than one commit per write"""
        insert_stmts = [f"INSERT INTO TWEETS(message) values('{tweet.text}');" for tweet in self.tweets]
        execute_multiple_inserts(insert_stmts=insert_stmts)
        
    def on_error(self, status_code):
        """ 420 code = too many API requests"""
        if status_code == 420:
            self.write_to_db()
            # returning False disconnects the stream
            return False
