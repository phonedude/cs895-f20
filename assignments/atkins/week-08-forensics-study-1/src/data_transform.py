from data_collection import slugify
from urllib.parse import urlparse
import json
import csv

def tweets_to_csv(slug, domain, writer):
    try:
        with open("../data/tweets/" + slug + ".json") as f:
            for line in f:
                js = json.loads(line)
                date = js.get("date")
                _id = js.get("id")
                username = js.get("username")
                writer.writerow([_id, date, username, domain])
    except:
        print("NO TWEETS FILE")


def parse_web_archive(url):
    components = urlparse(url)
    return components.hostname


def timemaps_to_csv(slug, domain, writer):
    try:
        with open("../data/timemaps/" + slug + ".json") as f:
            json_obj = json.load(f)
            for js in json_obj.get("mementos", {}).get("list", []):
                date = js.get("datetime")
                uri_m = js.get("uri")
                archive = parse_web_archive(uri_m)
                writer.writerow([uri_m, date, archive, domain])
    except Exception as e:
        print(e)
        print("NO TIMEMAP FILE")


if __name__ == "__main__":
    with open("../data/sample_alive.csv") as f, \
            open("../data/tweets_small.csv", 'w') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        writer.writerow(["id", "date", "username", "domain"])
        for row in reader:
            domain = row[0]
            urir = row[1]
            final_urir = row[2]
            status_code = row[3]
            print("Running on {}".format(domain))
            tweets_to_csv(slugify(domain), domain, writer)
    with open("../data/sample_alive.csv") as f, \
        open("../data/timemaps_small.csv", 'w') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        writer.writerow(["uri_m", "date", "archive", "domain"])
        for row in reader:
            domain = row[0]
            urir = row[1]
            final_urir = row[2]
            status_code = row[3]
            print("Running on {}".format(domain))
            timemaps_to_csv(slugify(domain), domain, writer)
