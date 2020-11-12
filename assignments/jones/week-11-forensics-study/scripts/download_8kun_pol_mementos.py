import requests
import sys
import json
import os

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

print("starting", flush=True)

with open("8ch-pol-timemap.json") as f:
    jdata = json.load(f)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})

retry = Retry(
    total=10,
    read=10,
    connect=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504)
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

for entry in jdata["mementos"]["list"]:

    print("examining entry {}".format(entry), flush=True)

    output_filename = 'pol-mementos/' + entry["datetime"] + '.html'
    headers_output_filename = 'pol-mementos/' + entry["datetime"] + '-headers.json'

    if not os.path.exists(output_filename):

        print("fetching {}".format(entry["uri"]), flush=True)

        try:
            r = requests.get(entry["uri"], headers={'user-agent': 'ODUCS-WSDL-experiment'})

        except requests.exceptions.ConnectionError as e:
            print("failed to download {}".format(entry["uri"]))

            with open(output_filename + '-download_error.date', 'w') as f:
                f.write(repr(e))
                continue

        if r.status_code == 200:

            with open(output_filename, 'w') as f:
                print("writing {} to {}".format(entry["uri"], output_filename), flush=True)
                f.write(r.text)
    
            with open(headers_output_filename, 'w') as f:
                print("writing headers from {} to {}".format(entry["uri"], headers_output_filename,), flush=True)
                json.dump(dict(r.headers), f)

        else:
            print("failed to download memento at {}, code was {}".format(entry["uri"], r.status_code))

            with open(output_filename + '-non200.dat', 'w') as f:
                f.write("{}".format(r.status_code))

print("done", flush=True)
