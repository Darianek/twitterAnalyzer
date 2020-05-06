import json
import math
from tweepy import Cursor
from twitter_client import get_twitter_client

import pymongo

myclient = pymongo.MongoClient('localhost', 27017)
mydb = myclient["twitterAnalyzer"]

users_collection = mydb["users"]
graph_collection = mydb["graphs"]

MAX_FRIENDS = 1500


def paginate(items, n):
    for i in range(0, len(items), n):
        yield items[i:i+n]

def get_user_data(user):
    
    if user.protected:
        users_data = {"_id": str(user.id),
                  "Label": user.screen_name,
                  "Followers Count": str(0),
                  "Friends Count": str(user.friends_count),
                  "Created at": str(user.created_at),
                  "Protected": user.protected,
                  "Location": str(0),
                  "Verified": user.verified,
                  "Listed count": str(user.listed_count),
                  "Favourites count": str(user.favourites_count),
                  "Status count": str(user.statuses_count),
                  "Default profile": user.default_profile,
                  "Default profile image": user.default_profile_image}
    else:
        if user.location:
            location = user.location
        else:
            location = str(0)
            
        users_data = {"_id": str(user.id),
                  "Label": user.screen_name,
                  "Followers Count": str(user.followers_count),
                  "Friends Count": str(user.friends_count),
                  "Created at": str(user.created_at),
                  "Protected": user.protected,
                  "Location": location,
                  "Verified": user.verified,
                  "Listed count": str(user.listed_count),
                  "Favourites count": str(user.favourites_count),
                  "Status count": str(user.statuses_count),
                  "Default profile": user.default_profile,
                  "Default profile image": user.default_profile_image}

    return users_data

def get_graph_data(user, source, target, direction):
    graph_data = {"_id": user.screen_name, user.screen_name: {"Source": source, "Target": target, "Direction": direction}}
    
    return graph_data

def get_sinlge_user(screen_name, access_file):
    
    
    client = get_twitter_client(access_file)

    account = client.get_user(screen_name)
    
    users_data = get_user_data(account)

    try:        
        users_collection.insert_one(users_data)
    except pymongo.errors.DuplicateKeyError:
        pass
    
    return users_data
    
def get_user(screen_name, access_file):

    client = get_twitter_client(access_file)

    account = client.get_user(screen_name)

    max_pages = math.ceil(MAX_FRIENDS / 5000)

    # get data for a given user

    source = []
    target = []
    direction = []
    connections = set()
    
    users_data = get_user_data(account)

    try:        
        users_collection.insert_one(users_data)
    except pymongo.errors.DuplicateKeyError:
        pass
    
    counter = 0
    if not account.protected:
        for followers in Cursor(client.followers_ids, screen_name=screen_name, count=1500).pages(max_pages):
            for chunk in paginate(followers, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    users_data = get_user_data(user)
                    source.append(str(account.id))
                    target.append(str(user.id))
                    direction.append('Directed')
                    connections.add(user.screen_name)
                    try:        
                        users_collection.insert_one(users_data)
                    except pymongo.errors.DuplicateKeyError:
                            continue
            counter += len(followers)
        for friends in Cursor(client.friends_ids, screen_name=screen_name, count=1500).pages(max_pages):
            for chunk in paginate(friends, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    users_data = get_user_data(user)
                    source.append(str(user.id))
                    target.append(str(account.id))
                    direction.append('Directed')
                    connections.add(user.screen_name)
                    try:        
                        users_collection.insert_one(users_data)
                    except pymongo.errors.DuplicateKeyError:
                            continue
            counter += len(friends)

    my_query = {"_id": str(account.id)}
    connections_data = {"$set": {"Connections": list(connections)}}
    users_collection.update_one(my_query, connections_data)
    graph_data = get_graph_data(account, source, target, direction)
    try:
        graph_collection.insert_one(graph_data)
    except pymongo.errors.DuplicateKeyError:
        pass

def get_number(screen_name, access_file):
    
    client = get_twitter_client(access_file)

    isProtected = client.get_user(screen_name).protected

    max_pages = math.ceil(MAX_FRIENDS / 5000)

    # get data for a given user

    group1 = set()
    group2 = set()
    people = set()

    counter = 0
    if not isProtected:
        for followers in Cursor(client.followers_ids, screen_name=screen_name, count=1500).pages(max_pages):
            for chunk in paginate(followers, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    people.add(json.dumps(user._json))
                    group1.add(json.dumps(user._json))
            counter += len(followers)
        for friends in Cursor(client.friends_ids, screen_name=screen_name, count=1500).pages(max_pages):
            for chunk in paginate(friends, 100):
                users = client.lookup_users(user_ids=chunk)
                for user in users:
                    people.add(json.dumps(user._json))
                    group2.add(json.dumps(user._json) + "\n")
            counter += len(friends)

    return len(people)