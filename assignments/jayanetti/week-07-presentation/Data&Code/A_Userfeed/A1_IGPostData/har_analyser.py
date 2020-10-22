import sys
import json
from haralyzer import HarParser, HarPage
from collections import Counter
from random import choice
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring


def extract_json(html):
	soup = BeautifulSoup(html, 'lxml')
	body = soup.find('body')
	#script_tag = body.find('script')
	#raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')   
	#print(a)
	script_tag = body.find('script', text=lambda t: t.startswith('window._sharedData'))
	raw_string = script_tag.string.split(' = ', 1)[1].rstrip(';')
	#.split(' = ', 1)[1].rstrip(';')
	#data = json.loads(page_json)
	#print(raw_string)
	return json.loads(raw_string)


def get_shortcode_first(res):
	json_data = extract_json(res)
	with open(sys.argv[2], "w") as f:
		f.write("shortcode,url,time_unix,time_utc,likes,comments\n")
		#print(json_data)
		try:
			#print("a")
			for j in range(0,12):
				shortcode = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["shortcode"]
				time = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["taken_at_timestamp"] 
				likes = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["edge_liked_by"]['count'] 	
				comments = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["edge_media_to_comment"]['count'] 	
				url = "https://www.instagram.com/p/%s/" % shortcode
				ts = int(time)
				utc = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				#print("a")
				f.write("%s,%s,%s,%s,%s,%s\n" % (shortcode,url,time,utc,likes,comments))		
		except Exception as e:
			print(e)
			pass
	#return shortcode_list1


def get_shortcode(res):
	json_data = json.loads(res)
	with open(sys.argv[2], "a") as g:
		#print(json_data)
		try:
			for j in range(0,12):
				shortcode = json_data['data']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["shortcode"]	
				#print(res)		
				time = json_data['data']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["taken_at_timestamp"] 
				likes = json_data['data']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["edge_media_preview_like"]['count'] 
				comments = json_data['data']['user']['edge_owner_to_timeline_media']["edges"][j]["node"]["edge_media_to_comment"]['count'] 
				url = "https://www.instagram.com/p/%s/" % shortcode
				ts = int(time)
				utc = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				g.write("%s,%s,%s,%s,%s,%s\n" % (shortcode,url,time,utc,likes,comments))	
		except Exception as e:
			#print(e)
			pass
	#return shortcode_list2



if __name__ == "__main__":
	with open(sys.argv[1], 'rb') as f:
		har = f.read()
		har_parser = HarParser(json.loads(har))
		har_page = HarPage('page_4', har_data=json.loads(har))
	x = len(har_page.entries)
	for i in range(0,x):
		resource_type = har_page.entries[i]['_resourceType']
		#print(resource_type)
		req_url = har_page.entries[i]['request']['url']
		if req_url == "https://www.instagram.com/katyperry/":
			#First 12 posts
			res = har_page.entries[0]['response']['content']['text']
			#print(res)
			first_12_posts = get_shortcode_first(res)
		elif resource_type == "xhr" and req_url.startswith("https://www.instagram.com/graphql/query/?query_hash="):
			#for other posts
			res = har_page.entries[i]['response']['content']['text']
			#print(res)
			other_posts = get_shortcode(res)
