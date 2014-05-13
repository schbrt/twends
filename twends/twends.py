import tweepy
import secret_pass
from flask import Flask
from flask_sockets import Sockets
try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)
sockets = Sockets(app)

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(StreamListener, self).__init__()

    def on_data(self, data):
        d = json.loads(data)
        if d['geo'] or d['place']:
            print d['text']
        return d

    def on_error(self, status):
        print status

def set_auth():
    keys = secret_pass.secret_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    return auth

def get_tweets(api, tag):
    """
    Returns queue of tweets with a given hashtag
    """
    tweets = api.search(q=tag, count=100)
    for i in range(len(tweets)):
        if tweets[i].geo:
            print tweets[i]
    return tweets

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

@app.route('/')
def main():
    auth = set_auth()
    api = tweepy.API(auth)
    trends = get_trends(api)#, 23424977)
    ears = StreamListener(api)
    stream = tweepy.Stream(auth, ears)
    while True:
        stream.filter(track=trends)

if __name__ == '__main__':
    app.run()