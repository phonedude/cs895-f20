#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime
import io
import csv
import re
import requests
from bs4 import BeautifulSoup
from csv import writer
from csv import reader



#Get the timemap for the URL
def check_memento(url):
	cmd = ("sudo docker run ibnesayeed/memgator %s" % url)
	a = os.popen(cmd)
	timemap = a.readlines()
	#print(timemap)
	with open("KatyPerryTimeMap.csv", "w") as f:
		for item in timemap:
			rel = (item.split("; ")[1]).split("=")[1]
			index = timemap.index(item)
			URIM = ""
			if rel == '"first last memento"':
				print("only one memento")
				#URIM = item.split("; ")[0].strip("<>")			
				#datetime = re.findall('"([^"]*)"', item.split("; ")[2])[0]
			elif rel == '"first memento"':
				#print("first_memento")
				#print(item)
				URIM = item.split("; ")[0].strip("<>")			
				datetime = re.findall('"([^"]*)"', item.split("; ")[2])[0]
			elif rel == '"memento"':
				#print("memento")	
				URIM = item.split("; ")[0].strip("<>")			
				datetime = re.findall('"([^"]*)"', item.split("; ")[2])[0]
			elif rel == '"last memento"':
				#print("last_memento")
				URIM = item.split("; ")[0].strip("<>")			
				datetime = re.findall('"([^"]*)"', item.split("; ")[2])[0]
			#try:
			if URIM:
				datetime = '"' + datetime + '"'
				f.write("%s,%s\n"  % (URIM,datetime))


def modify_date_time():
	URIM_list = []
	memento_datetime_list = []
	with open("KatyPerryTimeMap.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")
		URIM_list, Date =  zip(*reader)
		for URIM in URIM_list:
			print(URIM)
			response = requests.get(URIM)
			memento_datetime = None
			try:
				memento_datetime = response.headers['memento-datetime']
			except:
				print("No memento datetime for" + URIM)
			memento_datetime_list.append(memento_datetime)
		rows = zip(URIM_list, Date, memento_datetime_list)
		with open("KatyPerryTimeMapOut.csv", "w") as h:
			writer = csv.writer(h, delimiter=",")
			for row in rows:
				writer.writerow(row)



if __name__ == "__main__":
	#Get the timemap for the URL
	#url = "https://www.instagram.com/nerd_no.mad/"
	#url = "https://www.instagram.com/katyperry/"
	#check_memento(url)
	modify_date_time()





