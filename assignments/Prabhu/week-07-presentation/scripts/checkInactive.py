import sys
import requests

def sanitize(x):
    return "http://www." + x.replace(":80", "").replace("https", "http").split("/", 2)[-1].replace("www.", "")

fname = sys.argv[1]
with open(fname, “r”) as f:
    for url in f.read().split(“\n”):
resp = requests.get(url)
status_code = resp.status_code
if sanitize(resp.url) != sanitize(url):
    status_code = resp.history[0].status_code if len(resp.history) > 0 else status_code
if status_code != 200:
    print(url)



