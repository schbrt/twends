import tweepy
import key_config
from pymongo import MongoClient
from flask import Flask, render_template
try:
    import simplejson as json
except ImportError:
    import json


app = Flask(__name__)


def set_auth():
    """
    Connects to twitter api, returns tweepy auth object
    """
    keys = key_config.key_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    return auth


def get_tweets(api, trends):
    """
    Returns dictionary of lists of tweets for given hashtag
    """
    trend_dict = {}
    for trend in trends:
        tweets = api.search(q=trend, count=100)
        with_geo = []
        for i in range(len(tweets)):
            if tweets[i].geo:
                with_geo.append(tweets[i])
        trend_dict[trend] = with_geo
    return trend_dict


def get_trends(api, loc=1):
    """
    Returns a list of trending topics for the given location.
    Default location is WOEID = 1, worldwide
    """
    trend_dict = api.trends_place(loc)
    data = trend_dict[0]
    trend_list = data['trends']
    tags = [trend['name'] for trend in trend_list]
    return tags


def tweet_handler(api):
    """
    Calls functions to find trends, gets tweets based off of trends, then
    creates a dictionary of the form {trend: [list of tweets]}
    """
    trends = get_trends(api)  # , 23424977)
    trend_dict = get_tweets(api, trends)
    return trend_dict


def main():
    client = MongoClient()
    db = client.twends              # initialize and connect to mongodb
    auth = set_auth()
    api = tweepy.API(auth)       # connect to twitter api, retrive api wrapper
    trend_dict = tweet_handler(api)
    db.insert()                            # put retrieved tweets in mongodb
    for item in trend_dict:
        print len(item)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    main()
