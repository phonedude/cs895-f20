#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime
import io
import csv


def get_urls():
	with open("post_urls_cdx.txt", "r") as f:
		urls = f.readlines()
		return urls


def check_memento(urls):
	rel_list = []
	f= open("memento.csv","w+")
	f.close()
	print("Started collecting timemaps..")
	with open("memento.csv", "a") as f:
		for url in urls:
			cmd = ("sudo docker run ibnesayeed/memgator %s" % url)
			a = os.popen(cmd)
			timemap = a.readlines()
			if len(timemap) == 0:
				start_index = 1
				end_index = 0
			for item in timemap:
				rel = (item.split("; ")[1]).split("=")[1]
				if rel == '"first last memento"':
					start_index = 1
					end_index = 2
				elif rel == '"first memento"':
					start_index = timemap.index(item)
				elif rel == '"last memento"':
					end_index = timemap.index(item)
			memento_count = end_index - start_index + 1
			print(url, memento_count)
			#print("Started printing memento count..")
			f.write("%s,%s\n" % (url.strip("\n"), memento_count))
		print("Completed counting the number of mementos!")

def get_memento_count():
	memento_list = []
	with open("memento.csv", "r") as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			memento_list.append(row[1])
	print(memento_list)
	with open("memento.txt", "w") as g:
		for each in memento_list:
			g.write(each+"\n")
	cmd = ("sort memento.txt | uniq -c | awk '{print $2\",\"$1}' > memento_count.csv")
	b = os.popen(cmd)


if __name__ == "__main__":
	urls = get_urls()
	no_of_mementos =  check_memento(urls)
	#memento_count = get_memento_count()

	
