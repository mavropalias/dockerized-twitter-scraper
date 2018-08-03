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
    def on_tweet(self, tweet):
        rt = Tweet()

        rt.tweet_id = tweet["id"]
        rt.created_at = tweet["created_at"]
        rt.text = tweet["text"]
        rt.source = tweet["source"]
        rt.coordinates = tweet["coordinates"]
        rt.user_id = tweet["user_id"]
        rt.user_is_verified = tweet["user_is_verified"]
        rt.user_followers_count = tweet["user_followers_count"]
        rt.user_listed_count = tweet["user_listed_count"]

        rt.cleanup_and_analyze()

        self.collection.insert_one(tweet)
