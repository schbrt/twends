import tweepy
from textblob import TextBlob
import key_config
from flask import Flask, render_template
from flask.ext.socketio import SocketIO
try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)
socketio = SocketIO(app)


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        self.count = 0

    def on_data(self, data):
        self.count += 1
        data = json.loads(data)
        if data['coordinates'] is not None:
            tweet = {'id': data['id'], 'coords': data['coordinates'], 'text': data['text']}
            sent = TextBlob(tweet['text'])
            tweet['polarity'] = sent.sentiment.polarity
            print tweet
            jsontweet = json.dumps(tweet)
            self.handle_json(jsontweet)
        return True

    def on_error(self, status):
        print 'Error: ' + repr(status)

    @socketio.on('json')
    def handle_json(message):
        SocketIO.send(message, json=True)


def set_auth():
    """
    Connects to twitter api, returns tweepy auth object
    """
    keys = key_config.key_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    return auth


@app.route('/')
def initialize():
    auth = set_auth()
    listener = StreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(locations=[-180, -90, 180, 90], languages=['en'])

if __name__ == '__main__':
    socketio.run(app)
