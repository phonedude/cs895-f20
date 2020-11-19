import botometer
import base64
import os
import requests
import time
import json
from dateutil import parser
import re
import bs4
import datetime
import tweepy

rapidapi_key = "*"
twitter_app_auth = {
    'consumer_key': '*',
    'consumer_secret': '*',
    'access_token': '*',
    'access_token_secret': '*',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

def getBotReport():
    users = ["@" + x[1] for x in json.loads(open("users.json", "r").read())]
    responses = []
    for username in users:
        try:
            response = bom.check_account(username)
            responses.append([username, dict(response), 0])
        except tweepy.TweepError as e:
            responses.append([username, None, 1])
        except botometer.NoTimelineError as e:
            responses.append([username, None, 2])
        with open("bot_report.json", "w") as f:
            f.write(json.dumps(responses))
        print(f"Done {len(responses)}")

if __name__ == '__main__':
    getBotReport()