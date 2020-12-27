from nameko.rpc import rpc
from pymongo import MongoClient

from Tweet import Tweet


class ScraperMicroService:
    """
    Obulus scraper microservice
    """

    name = "scraper_microservice"
    client = MongoClient('mongodb', 27017)
    db = client.twitter
    collection = db.tweets

    @rpc
    def on_tweet(self, raw_tweet):
        tweet = Tweet(raw_tweet)
        self.collection.insert_one(tweet.toCleanDict())
