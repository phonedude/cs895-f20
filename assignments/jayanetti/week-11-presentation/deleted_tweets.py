#!/usr/bin/env python3

import os
import json
from datetime import date
from datetime import datetime
import io
import csv
import re
import bs4
import requests
from bs4 import BeautifulSoup
from csv import writer
from csv import reader


def get_live_tweets(UNs):
	for UN in UNs:
		# try:
		cmd = ("twint -u %s --timeline --since 2020-10-01 | cut -d' ' -f1 | sort > %s_live.id" % (UN, UN))
		a = os.popen(cmd)
			#print(a)
		# except:
		#  	pass

def get_timemap(UN):
	cmd = ("curl -s http://memgator.cs.odu.edu/timemap/link/https://twitter.com/%s | grep 'memento'" % (UN))
	a = os.popen(cmd)
	timemap = a.readlines()
	#print(timemap)		
	URIM_list = []
	filename = "%s_timemap.txt" % UN
	with open(filename, "a") as f:
		for item in timemap:
			#rel = (item.split("; ")[1]).split("=")[1]
			URIM = item.split("; ")[0].strip("<>")	
			date = re.findall('"([^"]*)"', item.split("; ")[2])[0]
			start_date = datetime.strptime("Sun, 01 Oct 2020 00:00:00 GMT", '%a, %d %b %Y %H:%M:%S GMT')
			date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
			#print(date)
			if date > start_date:
				URIM_list.append(URIM)
				f.write(URIM + "\n")
	return URIM_list



def get_archived_tweets(UN, URIM_list):	
	filename = "%s_archived.csv" % UN
	with open(filename, "w") as g:		
		for URIM in URIM_list:		
			response = requests.get(URIM)	
			html = response.text
			#print(html)
			soup = bs4.BeautifulSoup(html,"html.parser")
			match = soup.select('div.js-stream-tweet')
			#print(match_tweet_div_tag)
			for tag in match:
				#print(tag)
				if tag.has_attr("data-tweet-id"):
					if tag.has_attr("data-retweet-id"): 
						RT = True
						id =tag["data-retweet-id"]			
					else:
						RT = False
						id =tag["data-tweet-id"]					
					#print(id)
					tweets = tag.select('p.js-tweet-text.tweet-text') #get tweet text and other data if needed
					#print(tweets)
					timestamp = tag.find("span", {"class": "js-short-timestamp"})
					time = timestamp["data-time"]
					ts = int(time)
					start_date = datetime.strptime("Sun, 01 Oct 2020 00:00:00 GMT", '%a, %d %b %Y %H:%M:%S GMT')
					utc = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
					date = datetime.strptime(utc, '%Y-%m-%d %H:%M:%S')
					#print(id, utc)
					if date>start_date:
						g.write("%s, %s, %s\n" % (id, utc, RT))
					else:
						pass
	cmd = ("cat %s_archived.csv | cut -d',' -f1 | sort | uniq > %s_archived.id" % (UN, UN))
	a = os.popen(cmd)


def compare(UN):
	cmd = ("comm -13 %s_live.id %s_archived.id > %s_deleted.id" % (UN, UN, UN))
	a = os.popen(cmd)	



if __name__ == "__main__":
	deleted_urls = []
	#UNs = ["HimarshaJ"]
	#UNs = ["VP", "Mike_Pence", "GovAbbott", "GregAbbott_TX", "SenTomCotton", "TomCottonAR", "SenTedCruz", "tedcruz", "GovRonDeSantis", "RonDeSantisFL", "GovMikeDeWine", "MikeDeWine", "NikkiHaley", "GovLarryHogan", "LarryHogan", "HawleyMO", "SenMikeLee", "mikeleeforutah", "SecPompeo", "mikepompeo", "SenRubioPress", "marcorubio", "SenSasse", "BenSasse" ]
	UNs = ["VP", "Mike_Pence", "GovAbbott", "GregAbbott_TX", "SenTomCotton", "TomCottonAR", "SenTedCruz", "tedcruz", "GovRonDeSantis", "RonDeSantisFL", "GovMikeDeWine", "MikeDeWine", "NikkiHaley", "GovLarryHogan", "LarryHogan", "HawleyMO", "SenMikeLee", "mikeleeforutah", "SecPompeo", "mikepompeo", "SenRubioPress", "marcorubio", "SenSasse", "BenSasse","SenRickScott", "ScottforFlorida", "SenatorTimScott", "votetimscott", "TimScottSC", "SenKamalaHarris", "KamalaHarris", "SenBooker", "CoryBooker", "SenAmyKlobuchar", "amyklobuchar"]
	#tweets =  get_live_tweets(UNs)
	#print("Collected Live Tweets ====================================================")
	for UN in UNs:
		#URIM_list =  get_timemap(UN)
		#tweet_data = get_archived_tweets(UN, URIM_list)
		#sorted_ids = get_id(UN)
		#print("Collected Archive Tweets for %s ====================================================" % UN)
		deleted_tweets =  compare(UN)
	print("Collected Deleted Tweets ====================================================")
	for UN in UNs:
		file = "%s_deleted.id" % UN
		print(file)
		with open(file, "r") as f:
			ids = f.readlines()
			#print(ids)			
			for each_id in ids:
				each_id = each_id.strip("\n")
				url = "https://twitter.com/%s/status/%s" % (UN, each_id)	
				print(url)			
				headers = {'User-Agent': 'Googlebot'}
				response = requests.get(url, headers= headers, allow_redirects=False)
				status = response.status_code
				#print(status)
				if status != 200:
					#print("yes")
					if status == 302:
						location = response.headers['location']
					else:
						location = "null"
					item = url +"," + str(status) +"," + location						
					deleted_urls.append(item)
				else:
					pass
	with open("all_deleted_tweets.txt", "w") as g:
		for each in deleted_urls:
			#print(each)
			g.write(each+"\n")	

			
