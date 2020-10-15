import sys
fname = sys.argv[1]
with open(fname, “r”) as f:
	for url in f.read().split(“\n”):
print("http://www." + url.split("//", 1)[-1].lstrip("www.").rstrip("/").replace(“:80”, “”))

