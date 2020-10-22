import csv
import json
import random
import requests
import os.path
import logging
import unicodedata
import re
import twint
from urllib.parse import urlparse

log = logging.getLogger()
log.setLevel(logging.INFO)


def random_sample_csv(inputfile, outputfile, headers=True):
    """
    Randomly select lines from csv with/without headers
    and output to another file
    """
    with open(inputfile, 'r') as f, \
            open(outputfile, 'w') as out:
        if headers:
            headers = next(f)
        lines = f.read().splitlines()
        sample_lines = random.sample(lines, 100)
        # if headers:
        #     sample_lines = headers + sample_lines
        out.writelines("%s\n" % place for place in sample_lines)


def prepend_scheme(url) -> str:
    """
    Helper to add scheme to url from sample
    """
    components = urlparse(url)
    if not components.scheme:
        return "http://" + url
    return url


def live_web_check(uri):
    """
    Check live web for URI
    :return: status_code and final URI
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"
        }
        resp = requests.get(uri, headers=headers, verify=False)
        return resp
    except Exception as e:
        log.error("Could not request: {}".format(uri))
        log.error(e)
    return None


def get_timemap(url):
    """
    Get Memgator aggregation of timemaps for a uri
    """
    memgator_request = "http://localhost:1208/timemap/json/" + prepend_scheme(url)
    try:
        resp = requests.get(memgator_request)
        return resp
    except Exception as e:
        log.error("Memgator request failed with error {}".format(e))


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def run_live_check(csv_reader, outputfile):
    with open(outputfile, 'w') as out:
        writer = csv.writer(out, delimiter=',')
        for row in reader:
            uri_w_scheme = prepend_scheme(row[0])
            resp = live_web_check(uri_w_scheme)
            if resp is not None:
                print("Live check came back with: {}".format(resp.status_code))
                writer.writerow([row[0], uri_w_scheme, resp.url, resp.status_code])
            else:
                print("Live check came back with no response")
                writer.writerow([row[0], uri_w_scheme, "", ""])


def twitter_search_uri(uri):
    """
    Use twint to search twitter for tweet coverage of URIs
    """
    c = twint.Config()
    c.Search = "{}".format(uri)
    c.Output = "../data/tweets/" + slugify(uri) + ".json"
    c.Store_json = True
    # c.Lang = "en"
    c.Links = "include"
    # Limit tweets to 10000
    c.Limit = 10000
    twint.run.Search(c)


def save_cdx_count(uri, writer):
    count = 0
    try:
        cdx =  "http://web.archive.org/cdx/search/cdx?url={}&matchType=prefix".format(uri)
        resp = requests.get(cdx)
        for line in resp.iter_lines():
            count += 1
    except Exception as e:
        print("COULD NOT PROCESS", uri)
        print("Hit some exception", e)
    writer.writerow([uri, count])


if __name__ == "__main__":
    sample_csv = "../data/sample.csv"
    if not os.path.isfile(sample_csv):
        random_sample_csv("../data/fake_news_sites.csv", sample_csv)

    sample_alive = "../data/sample_alive.csv"
    with open(sample_csv) as f:
        reader = csv.reader(f)
        if not os.path.isfile(sample_alive):
            run_live_check(reader, sample_alive)

        # for row in reader:
        #     uri = row[0]
        #     timemap_file = "../data/timemaps/" + slugify(uri) + ".json"
        #     if not os.path.isfile(timemap_file):
        #         log.info("Getting timemap for {}".format(uri))
        #         resp = get_timemap(uri)
        #         if resp:
        #             with open(timemap_file, 'w') as f:
        #                 json.dump(resp.json(), f)

        #     tweet_file = "../data/tweets/" + slugify(uri) + ".json"
        #     if not os.path.isfile(tweet_file):
        #         # if not os.path.isfile(tweet_file):
        #         log.info("Getting tweets for {}".format(uri))
        #         twitter_search_uri(uri)

        cdx_count_file = "../data/cdx_counts.csv"
        if not os.path.isfile(cdx_count_file):
            with open(cdx_count_file, 'w') as out:
                writer = csv.writer(out)
                writer.writerow(["domain", "count"])
                for row in reader:
                    uri = row[0]
                    print("GETING CDX COUNT FOR", uri)
                    save_cdx_count(uri, writer)
