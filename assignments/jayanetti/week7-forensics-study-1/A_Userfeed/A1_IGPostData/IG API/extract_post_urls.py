
import json
import requests
from random import choice
from datetime import datetime
from bs4 import BeautifulSoup


def get_JSON():
	url = "https://instagramdimashirokovv1.p.rapidapi.com/feed/407964088/"

	#2nd page: QVFBZ09mMTk2ZTFLTmlpd0VqRGJHVW1qTjJQNUVCUHVSUm1wdmpDZ3g3cXlJei1vRy11ZzJwQTd5OUp3TjZSSGpfZi13M2tscS1xcDM3UUNIZkZoVlJtYQ=="
	#3rd page: QVFCcXFrVVVpSWQzTmdsWThlc0ZreWxEdWZrOUE1QVlTZVB1d1pQd1RvMUpCX24zXzQwV1Q5aFR5eGtqU0ZmVURENkZMbEtrdVdGem5FTlExMHBjRF9fdQ==

	headers = {
		'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com",
		'x-rapidapi-key': "3b2f084458msh0618ef1d4740a13p172c50jsn68c12b05836c"
	    }

	response = requests.request("GET", url, headers=headers)

	print(response.text)

def load_json():
	with open("post_urls.txt", "w") as g:
		for i in range(1,4):
			#f = open("json/%i.json", i) 
			filename = "json/%s.json" % i
			filename = str(filename)
			f = open(filename, "r")
			data = f.read()
			json_data = json.loads(data)
			for j in range(0,24):
				shortcode = json_data["edges"][j]["node"]["shortcode"]
				#print(shortcode)
				post_url = "https://www.instagram.com/p/%s/" % shortcode
				post_url = post_url + "\n"
				#print(post_url)
				g.write(post_url)


if __name__ == "__main__":
	#get_JSON()
	load_json()







# with open("katyperry_posts.json", "r") as f:
#         data = f.read()

# json_data = json.loads(data)
# print(json_data)
# metrics = json_data['edges']['node']['display_url']

# for m in metrics:
#     i_id = str(m['display_url'])
#     i_post_time = datetime.fromtimestamp(
#         m['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
#     i_likes = int(m['edge_liked_by']['count'])
#     i_comments = int(m['edge_media_to_comment']['count'])
#     i_media = m['display_url']
#     i_video = bool(m['is_video'])
#     print(i_id)
