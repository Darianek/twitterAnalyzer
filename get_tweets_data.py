import tweepy
import pandas as pd
import sys

from func_timeout import func_timeout, FunctionTimedOut

from time import strftime
from twitter_client import get_twitter_client

fname = sys.argv[1]
access_file = sys.argv[2]
ids = pd.read_csv(fname)
list_of_ids = ids['Id'].to_list()
listf_of_labels = ids['label'].to_list()

client = get_twitter_client(access_file)

tweets = []
labels = []
counter = 0

def get_tweet(client, number):
    tweet = client.get_status(number)
    
    return tweet

print('STARTING AT ' + strftime("%Y-%m-%d %H:%M:%S"))
for index, number in enumerate(list_of_ids):
    try:
        tweet = func_timeout(5, get_tweet, args=(client, number))
        tweets.append(tweet.text)
        labels.append(listf_of_labels[index])
        counter += 1
        if counter % 100 == 0:
            print(str(counter) + ' DONE AT ' + strftime("%Y-%m-%d %H:%M:%S"))
    except (FunctionTimedOut, tweepy.TweepError):
        print("Timed out! " + str(number) + ' tweet is unavailable')
name = 'train_{}.csv'.format(fname.split('.')[0])
df_dict = {'Tweet': tweets, 'label': labels}
df = pd.DataFrame(df_dict)
df.to_csv(name, index=False)
print('PROGRAM FINISHED AT ' + strftime("%Y-%m-%d %H:%M:%S"))