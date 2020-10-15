import tweepy
import sys

consumer_key = "*"
consumer_secret = "*"
access_token = "*"
access_token_secret = "*"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
with open(sys.argv[1], “r”) as f:
    for user in f.read().split(“\n”):
           for tweet in tweepy.Cursor(api.user_timeline,id=user, tweet_mode = "extended").items():
                print(f"https://twitter.com/twitter/statuses/{tweet.id} {tweet.full_text}")


