import sys
import re
import requests
pattern = pattern = re.compile(r"[^a-zA-Z](amy|barrett|coney)[^a-zA-Z]", re.IGNORECASE)
fname = sys.argv[1]
with open(fname, “r”) as f:
	for url in f.read().split(“\n”):
resp = requests.get(url)
if “html” in resp.headers[“Content-Type”] and pattern.search(resp.content.decode(“urf-8”):
	print(url)

