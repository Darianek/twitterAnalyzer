import tweepy
from tweepy import Cursor
from twitter_client import get_twitter_client
from twitter_misinformation import *

import pymongo

myclient = pymongo.MongoClient('localhost', 27017)
mydb = myclient["twitterAnalyzer"]

users_collection = mydb["users"]
graph_collection = mydb["graphs"]
tweets_collection = mydb["tweets"]

def check_by_tweets(screen_name, access_file):

    client = get_twitter_client(access_file)

    tweets = []
    positive = []
    negative = []
    
    ids = []
    dates = []
    
    check = tweets_collection.count_documents({"_id": screen_name})
    
    if check == 1:
        print('Already in database!')
    else:
        try:
            current_user = client.get_user(screen_name)
        
            if not current_user.protected:
                for page in Cursor(client.user_timeline, screen_name=screen_name, count=200).pages(16):
                    for status in page:
                        ids.append(str(status.id))
                        dates.append(status.created_at)
                        tweets.append(status.text)
                
                tweet_data = {"_id": screen_name, screen_name: {"_id": ids, "Text": tweets, "Created at": dates}}
                tweets_collection.insert_one(tweet_data)
            else:
                tweet_data = {"_id": screen_name}
                tweets_collection.insert_one(tweet_data)
                
        except tweepy.error.TweepError:
            print(screen_name + ' NOT EXISTS!')

    for tweet in tweets:
        result = check_tweet(tweet)
        
        if result:
            positive.append(1)
        else:
            negative.append(1)
    
    if len(positive) > len(negative):
        return True
    else:
        return False
