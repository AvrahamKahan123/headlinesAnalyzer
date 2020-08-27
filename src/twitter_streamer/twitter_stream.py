import tweepy, time
from twitter_streamer import Tweet


class TwitterListener(tweepy.StreamListener):
    """ Stream establishes single persistent connection to stream realtime tweets"""
    def __init__(self, time_limit=300):
        self.start_time = time.time()
        self.limit = time_limit
        self.tweets = []
        super(TwitterListener, self).__init__()

    def add_tweet(self, new_tweet: Tweet):
        self.tweets.append(new_tweet)


    def on_status(self, status):
        if not hasattr(status, "retweeted_status") and status.lang == "en":
            tweet_obj = self.construct_tweet(status)
            self.add_tweet(tweet_obj)
        self.check_time()

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
            return False

    def on_error(self, status_code):
        if status_code == 420:
            # returning False disconnects the string
            return False



