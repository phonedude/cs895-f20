import base64
import os
import requests
import sys
import bs4
import re
import datetime

urls = open(sys.argv[1], 'r').read().splitlines()
fw = open(sys.argv[2], "w")


for url in urls:
	dtime='-'
	soup = bs4.BeautifulSoup(requests.get(url).content, features="html.parser")
	for tweet in soup.findAll(class_ = "tweet"):
		if tweet.find(class_="tweet-text"):
			tweet_id = tweet["data-tweet-id"]
			text = tweet.find(class_="tweet-text").get_text()
			text = re.sub(r"[\n\t]*", "", text)
		if tweet.find(class_="username") and tweet.find(class_="username").b:
			if tweet.find(class_="_timestamp"):
				dtime = datetime.datetime.fromtimestamp(int(tweet.find(class_="_timestamp").attrs["data-time"]))
			username = tweet.find(class_="username").b.get_text()

		fw.write(f"{tweet_id}\t{username}\t{dtime}\t{text}\n")
