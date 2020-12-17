#!/usr/bin/env bash\

# everylegalvote
curl -s "http://web.archive.org/cdx/search/cdx?url='"$1"'&matchType=prefix" | sort -u -k 3 | awk '{print "https://web.archive.org/web/" $2 "/" $3};' | wc -l
curl -s "http://memgator.cs.odu.edu/timemap/link/'"$1"'" | grep datetime | awk '{print $1}' | awk -v FS=/ '{print $3}' | sort | uniq -c | sort -n
