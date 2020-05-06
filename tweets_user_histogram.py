from bs4 import BeautifulSoup
import requests
import json
import csv
import sys
import calendar
import os
import time
import math
from time import strftime
from datetime import datetime

import tweepy
from tweepy import Cursor
from twitter_client import get_twitter_client

from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


def countoccurrences(store, value):
    try:
        store[value] = store[value] + 1
    except KeyError:
        store[value] = 1
    return


if __name__ == '__main__':

    fname = 'data/for_tweets.txt'
    tmpname = 'data/tmptwt.txt'

    access_file = sys.argv[1]
    screen_name = sys.argv[2]
    period = sys.argv[3]

    if period == 'all':
        client = get_twitter_client(access_file)

        counter = 0
        tweets = []
        dates = Counter()

        current_user = client.get_user(screen_name)

        if not current_user.protected:
            for page in Cursor(client.user_timeline, screen_name=screen_name, count=200).pages(16):
                for status in page:
                    tweets.append(status.created_at.year)
                    counter += 1
        a = Counter(sorted(tweets))

        y_pos = np.arange(len(a.keys()))

        plt.bar(y_pos, a.values(), align='center', alpha=0.5)
        plt.xticks(y_pos, a.keys())
        plt.ylabel('Number of tweets')
        plt.title(screen_name + ' has ' + str(counter) + ' tweets')
        plt.show()

    elif period == 'year':
        date_wanted = sys.argv[4]

        client = get_twitter_client(access_file)

        counter = 0
        tweets = []
        dates = Counter()

        current_user = client.get_user(screen_name)

        if not current_user.protected:
            for page in Cursor(client.user_timeline, screen_name=screen_name, count=200).pages(16):
                for status in page:
                    if str(status.created_at.year) == str(date_wanted):
                        tweets.append(status.created_at.month)
                        counter += 1

        a = {}

        for i in range(1, 13):
            a.update({i: 0})

        b = Counter(sorted(tweets))

        a.update(b)

        keys = []

        for key in a.keys():
            keys.append(calendar.month_name[key])
        y_pos = np.arange(len(a.keys()))

        plt.bar(y_pos, a.values(), align='center', alpha=0.5)
        plt.xticks(y_pos, keys, rotation='45')
        plt.ylabel('Number of tweets')
        plt.title(screen_name + ' posted ' + str(counter) + ' tweets in ' + str(date_wanted))
        plt.show()

    elif period == 'month':
        date_wanted = sys.argv[4]

        client = get_twitter_client(access_file)

        counter = 0
        tweets = []
        dates = Counter()

        current_user = client.get_user(screen_name)

        if not current_user.protected:
            for page in Cursor(client.user_timeline, screen_name=screen_name, count=200).pages(16):
                for status in page:
                    if (str(status.created_at.year) + '-' + str(status.created_at.month)) == str(date_wanted):
                        tweets.append(status.created_at.day)
                        counter += 1

        strDate = str(date_wanted)
        objDate = datetime.strptime(strDate, '%Y-%m')

        days_number = calendar.monthrange(objDate.year, objDate.month)[1]

        a = {}

        for i in range(1, days_number + 1):
            a.update({i: 0})

        b = Counter(sorted(tweets))

        a.update(b)

        y_pos = np.arange(len(a.keys()))

        plt.bar(y_pos, a.values(), align='center', alpha=0.5)
        plt.xticks(y_pos, a.keys(), rotation='45')
        plt.ylabel('Number of tweets')
        plt.title(screen_name + ' posted ' + str(counter) + ' tweets in ' + str(date_wanted))
        plt.show()
