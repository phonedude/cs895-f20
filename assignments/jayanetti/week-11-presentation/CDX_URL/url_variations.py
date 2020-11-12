#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime
import io
import csv
import sys 
import pandas

filename = "url_var.csv"
finaldata = "Final_data.csv"
out = "Final_data_url_variations.csv"


def check_variations(filename):
	url_dic = {}	
	urls = []
	with open(filename, "r") as f:
		lines = f.readlines()
	for each in lines:
		#print(each)
		code, url = each.split(",",1)
		url = url.strip("\n")
		#url_dic[code] = [url]
		if code in url_dic:
			urls = url_dic[code]
			urls.append(url)
			url_dic[code] = urls
		else:
			url_dic[code] = [url]
	#print(len(url_dic["pe0gUfP-Xa"]))
	return url_dic

def file_csv(url_dic):
	data = pandas.read_csv(finaldata, header=None)
	print(data)
	shortcode = list(data[0])
	date = list(data[1])
	likes = list(data[2])
	comments = list(data[3])
	mementos = list(data[4])
	no_url_variations = []
	url_variations = []
	for item in shortcode:
		urls = []
		if item in url_dic:
			urls= url_dic[item]
			count = len(urls)
		else:
			urls = []
			count = 0
		url_variations.append(','.join(str(x) for x in urls))
		no_url_variations.append(count)
	rows = zip(shortcode, date, likes, comments, mementos, no_url_variations, url_variations)
	with open(out, "w") as h:
		writer = csv.writer(h, delimiter=",")
		for row in rows:
			writer.writerow(row)



if __name__ == "__main__":
	url_dic = check_variations(filename)
	file_csv(url_dic)