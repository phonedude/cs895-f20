#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime
import io
import csv
import sys 

def get_urls():
	with open(sys.argv[1], "r") as f:
		urls = f.readlines()
		return urls


def check_memento(urls):
	#with open("cdxdata.txt", "a") as g:
		for url in urls:
			url = url.strip("\n")
			cmd = ('curl "http://web.archive.org/cdx/search/cdx?url=%s"' % url)
			b = os.popen(cmd)
			break
			#g.write(b)



if __name__ == "__main__":
	urls = get_urls()
	no_of_mementos =  check_memento(urls)

	
