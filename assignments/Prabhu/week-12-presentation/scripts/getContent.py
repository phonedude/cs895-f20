import base64
import os
import requests
import time
import json

def checkAndGetData():
    if os.path.isfile("./data.json"):
        with open("./data.json", "r") as f:
            return json.loads(f.read())
    urls = json.loads(open("urls.txt", "r").read())
    data = []
    print(f"Total pages {len(urls)}")
    c = 0
    start = time.time()
    for url in urls:
        content = requests.get(url).content
        encoded = base64.b64encode(content).decode("ascii")
        data.append((url, encoded))
        c += 1
        if c % 10 == 0:
            print(f"Done {c} of {len(urls)} | Time taken - {time.time() - start}")
            start = time.time()
    with open("data.json", "w") as f:
        f.write(json.dumps(data))
    return data

if __name__ == '__main__':
    checkAndGetData()