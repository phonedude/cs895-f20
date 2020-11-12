#!/bin/bash

# Twint twitter scrape verified accounts that contained antifa.com
twint -s antifa.com --verified > antifa_verified.dat

# Twint twitter scrape unverified accounts that contained antifa.com
twint -s antifa.com > antifa_unverified.dat

# curl antifa.com to get its response
curl -i antifa.com > antifa_curl.dat

# Curl memgator for distribution of mementos per archive
curl -s http://memgator.cs.odu.edu/timemap/link/https://antifa.com | grep datetime | awk '{print $1}' | awk -v FS=/ '{print $3}' | sort | uniq -c | sort -n > archive_distribution.dat
