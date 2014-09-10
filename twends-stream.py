import tweepy
from textblob import TextBlob
import key_config
from flask import Flask, render_template
try:
    import simplejson as json
except ImportError:
    import json


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        self.count = 0

    def on_data(self, data):
        self.count += 1
        #print self.count
        data = json.loads(data)
        tweet = dict()
        if data['coordinates'] is not None:
            tweet = {'id': data['id'], 'coords': data['coordinates'], 'text': data['text']}
            sent = TextBlob(tweet['text'])
            print sent.sentiment
            print tweet['text']
            jsontweet = json.dumps(tweet)
        #print data
        return True

    def on_error(self, status):
        print 'Error: ' + repr(status)


def set_auth():
    """
    Connects to twitter api, returns tweepy auth object
    """
    keys = key_config.key_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    return auth


if __name__ == '__main__':
    auth = set_auth()
    api = tweepy.API(auth)                         # connect to twitter api, retrive api wrapper
    listener = StreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(locations=[-180, -90, 180, 90], languages=['en'])
