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


# 1. For a particular user: get the timemap for account page.
#   UROM, Datetime
# 2. For each memento: 
# 	Try: 
# 		extract date & follower count
# 	Except:
# 		pass


def get_urls():
	URIM_tuplist = []
	with open("KatyPerryTimeMapOut.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")
		for i in reader:
			#print(i[0])
			URIM_tuple = (i[0],i[2])
			URIM_tuplist.append(URIM_tuple)
	return URIM_tuplist


def get_follower_count(html, memento_date):
	follower_count = None
	soup = BeautifulSoup(html, "lxml")
	date = datetime.strptime(memento_date, '%a, %d %b %Y %H:%M:%S GMT')
	date1 = datetime.strptime("Mon, 12 Nov 2012 08:59:33 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date2 = datetime.strptime("Thu, 16 May 2013 06:55:25 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date3 = datetime.strptime("Sat, 25 Jan 2014 11:08:02 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date4 = datetime.strptime("Sat, 10 Jan 2015 00:44:52 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date5 = datetime.strptime("Tue, 20 Jan 2015 07:41:10 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date6 = datetime.strptime("Thu, 15 Oct 2015 13:08:10 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	date7 = datetime.strptime("Sun, 07 Feb 2016 21:59:24 GMT", '%a, %d %b %Y %H:%M:%S GMT') #FIXXX
	date8 = datetime.strptime("Fri, 17 Feb 2017 03:20:07 GMT", '%a, %d %b %Y %H:%M:%S GMT')
	try:
		if date1<=date<date2:
			#print("CASE 1")
			follower_count = case1(soup)
		elif date2<=date<date3:
			#print("CASE 2")
			follower_count = case2(soup)
		elif date3<=date<date4:
			#print("CASE 3")
			follower_count = case3(soup)
		elif date4<=date<date5:
			#print("CASE 4")
			follower_count = case4(soup)
		elif date5<=date<date6:
			#print("CASE 5")
			follower_count = case5(soup)
		elif date6<=date<date7:
			#print("CASE 6")
			follower_count = case6(soup)
		elif date7<=date<date8:
			#print("CASE 7")
			follower_count = case7(soup)
		elif date8<=date:
			#print("CASE 8")
			follower_count = case8(soup)
	except:
		pass	
	return follower_count


def case1(soup):			
	script_tag = soup.find_all('script') 
	#print(type(script_tag))
	list = []
	for tag in script_tag:
		text = tag.contents
		list.append(text)
	for each in list:
		#each = str(each[0])
		text = "None"
		try:
			text= each[0]
		except Exception as e:
			#print(e)
			pass
		if text.startswith("\nwindow._jscalls"):
			#print(type(text))
			a = text.split(' = ', 1)[1]
			string = a.split(',', 2)[2].strip("[").strip("]")
			#c =b.split(',', 9)[:9]
			#print(b)
			occur = 9  # on which occourence you want to split
			indices = [x.start() for x in re.finditer(",", string)]
			raw_string = string[0:indices[occur-1]]
			#print(raw_string)
			json_data = json.loads(raw_string)
			follower_count = json_data['counts']['followed_by']
			#print(follower_count)				
	return follower_count


def case2(soup):			#
	script_tag = soup.find_all('script') 
	#print(script_tag)
	list = []
	for tag in script_tag:
		text = tag.contents
		list.append(text)
	text = list[8][0]
	text = text.split("{",2)[2]
	text = text.rsplit("}",1)[0]
	raw_string = "{" + text + "}"
	#print(text)
	json_data = json.loads(raw_string)
	follower_count = json_data["props"]["user"]["counts"]["followed_by"]
	return follower_count

def case3(soup):			#
	script_tag = soup.find_all('script') 
	#print(script_tag)
	list = []
	for tag in script_tag:
		text = tag.contents
		list.append(text)
	text = list[8][0]
	raw_string = text.split(' = ', 1)[1].rstrip(';')
	json_data = json.loads(raw_string)
	follower_count = json_data["entry_data"]["UserProfile"][0]["user"]["counts"]["followed_by"]
	return follower_count

def case4(soup):
	for tag in soup.find_all("meta"):
		#print(tag)
		name = tag.get("name")
		if name == "description":
			description = tag.get("content")
			#print(description)			
			try:		
				#print(description)
				follower_count = description.split(", ")[0].split("; ")[1].split(" ")[0]
				print(follower_count)
			except Exception as e:
				#print(e)
				pass
			return follower_count

def case5(soup):
	for tag in soup.find_all("div"):
		#print(tag)		
		name = tag.get("class")
		#print(name)
		try:
			if name[0] == "user-stats":
				bullets = tag.contents[1]
				items = bullets.findAll('li')
				follower_count = items[1].findAll("span")[0].contents[0]
				#print(follower_count)
		except Exception as e:
			#print(e)
			pass
	return follower_count

def case6(soup):
	for tag in soup.find_all("span"):
		#print(tag)		
		name = tag.get("class")
		#print(name)
		try:
			if name[0] == "-cx-PRIVATE-FollowedByStatistic__count":
				follower_count = tag.contents[0]
				#print(tag.findAll("span"))
		# 		follower_count = items[1].findAll("span")[0].contents[0]
				#print(follower_count)
		except Exception as e:
		# 	#print(e)
			pass
	return follower_count

def case7(soup):			#
	script_tag = soup.find_all('script') 
	#print(script_tag)
	list = []
	for tag in script_tag:
		text = tag.contents
		list.append(text)
	try:
		text = list[11][0]
		raw_string = text.split(' = ', 1)[1].rstrip(';')
		json_data = json.loads(raw_string)	
		follower_count = json_data["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
	except:			
		text1 = list[23][0]
		#print(text1)
		raw_string = text1.split(' = ', 1)[1].rstrip(';')
		#print(raw_string)
		json_data = json.loads(raw_string)	
		follower_count = json_data["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
	return follower_count

def case8(soup):			
	for tag in soup.find_all("meta"):
		#print(tag)
		name = tag.get("name")
		if name == "description":
			description = tag.get("content")
			#print(description)			
			try:		
				#print(description)
				follower_count = description.split(", ")[0].split(" ")[0]
				#print(follower_count)
			except Exception as e:
				#print(e)
				pass
			return follower_count

def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)


def check_mapping():
	follower_count_list = []
	with open("KatyPerryTimeMap_Followers.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")
		for i in reader:
			#print(i[0])
			follower_count = i[3]
			follower_count_list.append(follower_count)
	new_list = []
	for item in follower_count_list:
		if "m" in item:
			if item == "Welcome":
				#print("jkkkkkkkkkk")
				item = 0
			else:
				#print("yes")
				item = float(item.strip("mn"))		
		else:
			try:
				item = int(item)
				item = float(item/1000000)
			except:
				item = 0
		item = "{:.2f}".format(item)
		if item == "0.00":
			print("yesssssssssss")
			item = None

		print(item)
		new_list.append(item)
	#print(new_list)
	add_column_in_csv('KatyPerryTimeMap_Followers.csv', 'KatyPerryTimeMap_Followers_Final.csv', lambda row, line_num: row.append(new_list[line_num - 1]))



if __name__ == "__main__":
	#Get the timemap for the URL
	#no_of_mementos =  check_memento(url)
	#Get the list of URIM
	URIM_tuplist = get_urls()
	follower_count_list = []
	#For each URIM, Get the response	
	for URIM, memento_date in URIM_tuplist:
		response = requests.get(URIM)
		html = response.text
		try:
			follower_count = get_follower_count(html, memento_date)
		except:
			follower_count = None
		print(URIM, follower_count)
		follower_count_list.append(follower_count)
	add_column_in_csv('KatyPerryTimeMapOut.csv', 'KatyPerryTimeMap_Followers.csv', lambda row, line_num: row.append(follower_count_list[line_num - 1]))
	check_mapping()


"""
FIX

* Date7
* other archives - ignore
* login page ones - discard
* map m, mn -> count

"""