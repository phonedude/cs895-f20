import base64
import os
import requests
import time
import json
from dateutil import parser
import re
import bs4
import datetime

pattern = re.compile(r"\B(\#[a-zA-Z]+\b)")
user_pattern = re.compile(r"\B(\@[a-zA-Z0-90-9_]+\b)")
date_pattern = re.compile(r'(\d+)')

def getUsers():
    if os.path.isfile("./users.json"):
        with open("./users.json", "r") as f:
            users = []
            for user in json.loads(f.read()):
                users.append((parser.parse(user[0]), user[1]))
            return users
    data = json.loads(open("data.json", "r"))
    usernames = []
    start = time.time()
    c = 0
    for item in data:
        content = item[1]
        dtime = parser.parse(date_pattern.findall(item[0])[0])
        decoded = base64.b64decode(content)
        soup = bs4.BeautifulSoup(decoded, features="html.parser")
        for tweet in  soup.findAll(class_ = "tweet"):
            if tweet.find(class_="username") and tweet.find(class_="username").b:
                if tweet.find(class_="_timestamp"):
                    dtime = datetime.datetime.fromtimestamp(int(tweet.find(class_="_timestamp").attrs["data-time"]))
                username = tweet.find(class_="username").b.get_text()
                usernames.append((dtime, username))
        c += 1
        if c % 10 == 0:
            print(f"Done {c} of {len(data)} | Time taken - {time.time() - start} | Number of Users - {len(usernames)}")
            start = time.time()
    with open("users.json", "w") as f:
        f.write(json.dumps(usernames, default=str))
    return usernames

if __name__ == '__main__':
    getUsers()