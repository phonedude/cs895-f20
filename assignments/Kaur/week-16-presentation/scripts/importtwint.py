import twint
import requests
import sys
import os
import json
import bs4
import time

def getActiveTweetIds(username):
    fname = "./active.tweets.json"
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return set(json.loads(f.read()))
    c = twint.Config()
    c.Username = username
    c.Hide_output = True
    c.Pandas = True
    twint.run.Search(c)
    ids = set([int(x) for x in twint.storage.panda.Tweets_df["id"].values])

    with open(fname, "w") as f:
        f.write(json.dumps(list(ids)))
    return ids

def getArchivedTweetIds(username):
    fname = "./archived.tweets.json"
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return set(json.loads(f.read()))

    url = f"http://web.archive.org/cdx/search/cdx?url=http://www.twitter.com/{username}/status/&matchType=prefix"
    res = requests.get(url).content.decode("utf-8").split("\n")
    urls = list(filter(lambda x: bool(x), map(lambda r: r.split(" ")[2] if len(r.split(" ")) > 4 and r.split(" ")[4] == "200" else "", res)))
    ids = []
    for u in urls:
        if u and u.split("/")[5].split("?")[0].isnumeric():
            ids.append(int(u.split("/")[5].split("?")[0]))

    with open(fname, "w") as f:
        f.write(json.dumps(ids))
    return set(ids)

def getArchivedLookup(username):
    fname = "./lookup.tweets.json"
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return json.loads(f.read())

    url = f"http://web.archive.org/cdx/search/cdx?url=http://www.twitter.com/{username}/status/&matchType=prefix"
    res = requests.get(url).content.decode("utf-8").split("\n")
    urls = list(filter(lambda x: bool(x[0]), map(lambda r: (
        r.split(" ")[2], f"http://web.archive.org/web/{r.split(' ')[1]}_id/{r.split(' ')[2]}"
    ) if len(r.split(" ")) > 4 and r.split(" ")[4] == "200" else [""], res)))
    lookup = {}
    for u in urls:
        if len(u) > 1 and u[0] and u[0].split("/")[5].split("?")[0].isnumeric():
            lookup[int(u[0].split("/")[5].split("?")[0])] = u[1]

    with open(fname, "w") as f:
        f.write(json.dumps(lookup))
    return lookup

def getDeletedTweets(username):
    fname = "./deleted.tweets.json"
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return set(json.loads(f.read()))
    deletedIds = getArchivedTweetIds(username) - getActiveTweetIds(username)
    with open(fname, "w") as f:
        f.write(json.dumps(list(deletedIds)))
    return deletedIds

def getDeletedTweetText(username):
    fname = "./tweets.json"
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            return json.loads(f.read())

    text_list = []
    deletedIds = getDeletedTweets(username)
    lookup = getArchivedLookup(username)
    c = 0
    start = time.time()
    for id in deletedIds:
        try:
            soup = bs4.BeautifulSoup(requests.get(lookup[str(id)]).content, "html.parser")
            if soup.find(class_="TweetTextSize--jumbo"):
                text = soup.find(class_="TweetTextSize--jumbo").get_text()
                text_list.append((id, text))
            c += 1
            if c % 5 == 0:
                print(f"Tweets done {c} / {len(deletedIds)} | Time taken - {time.time() - start}")
                start = time.time()
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt - Returning from function")
            return
        except Exception as e:
            print(f"Failed for {id} - {e}")
    with open(fname, "w") as f:
        f.write(json.dumps(list(text_list)))
    return text_list
            
    

if __name__ == '__main__':
    username = "neeratanden"
    getDeletedTweetText(username)
