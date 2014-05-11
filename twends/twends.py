import tweepy
import secret_pass
try:
    import simplejson as json
except ImportError:
    import json


def connect_api():
    keys = secret_pass.secret_dict()
    auth = tweepy.auth.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    #auth.set_access_token(keys['access_key'], keys['access_secret'])
    api = tweepy.API(auth)
    return api

def get_tweets(api, tag):
    """
    Returns queue of tweets with a given hashtag
    """
    tweets = api.search(tag)
    print len(tweets)

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

def main():
    api = connect_api()
    trends = get_trends(api,23424977)
    for tag in range(len(trends)):
        get_tweets(api, trends[tag])
if __name__ == '__main__':
    main()