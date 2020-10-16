import sys
import json
from haralyzer import HarParser, HarPage
from collections import Counter
import dateutil, datetime
import numpy as np

with open(sys.argv[1], 'rb') as f:
	har_parser = HarParser(json.loads(f.read()))

### ACCESSING FILES ###
#f=open(sys.argv[2], 'w')

timelist=[]
entries = []

for har_page in har_parser.pages:
	for entry in har_page.entries:
		#entries.append(entry)
		#date=entry['startedDateTime']
		#timelist.append(dateutil.parser.parse(date))
		url=entry['request']['url']
		if 'adaptive.json' in url:
			#print(url)
			cont=entry['response']['content']['text'] #['globalObjects']['tweets']			
			print(cont)
		# status=entry['response']['status']
		# method=entry['request']['method']
		# mtype=entry['response']['content']['mimeType']
		# out=f"{date}\t{url}\t{status}\t{method}\t{mtype}\n"
		# f.write(out)

f.close()