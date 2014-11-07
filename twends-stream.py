import tweepy
import json
from textblob import TextBlob
import key_config
from flask import Flask, render_template
from flask.ext.socketio import SocketIO


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
            #jsontweet = json.dumps(tweet)
            self.handle_json(tweet)
        return True

    def on_error(self, status):
        print 'Error: ' + repr(status)

    def handle_json(self, json):
        socketio.emit('event', json, namespace='/data')
        print('received json: ' + str(json))


def set_auth():
    """
    Connects to twitter api, returns tweepy auth object
    """
    keys = key_config.key_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    return auth


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/data')
def initialize():
    print 'Socket connection opened.'
    auth = set_auth()
    listener = StreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(locations=[-180, -90, 180, 90], languages=['en'])

if __name__ == '__main__':
    socketio.run(app)
