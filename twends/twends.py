import tweepy
import secret_pass
try:
    import simplejson as json
except ImportError:
    import json


def connect_api():
    keys = secret_pass.secret_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_key'], keys['access_secret'])
    api = tweepy.API(auth)
    return api

def main():
    api = connect_api()
    trends = api.trends_place(1)

if __name__ == '__main__':
    main()