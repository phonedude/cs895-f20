import tweepy
import sys

consumer_key = "*"
consumer_secret = "*"
access_token = "*"
access_token_secret = "*"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
for page in tweepy.Cursor(api.followers, screen_name=sys.argv[1]).pages():
    for user in [x.screen_name for x in page]:
print(user)


