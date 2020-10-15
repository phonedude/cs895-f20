# save CDX response to file
import requests
import sys
import csv

file = "katy_perry_posts.csv"
file_mementos = "ShortcodeVsNoOfMementos.csv"

def read_csv():
	post_data = {}
	with open(file, "r") as f:
		data = csv.reader(f)		
		for rows in data:
			mydict = {}
			code = rows[0]
			mydict["time"] = rows[3]
			mydict["likes"] = rows[4]
			post_data[code] = mydict
	#print(post_data)
	return post_data


def read_mementos():
	memento_data = {}
	with open(file_mementos, "r") as g:
		data = csv.reader(g)		
		for rows in data:
			code = rows[0]
			mementos = rows[1]
			memento_data[code] = mementos
	#print(memento_data)
	return memento_data
			

def combine(post_data,memento_data):
	for key in post_data:
		code = key
		if code in memento_data:
			mementos = memento_data[code]
			post_data[code]["mementos"] = mementos
		else:
			post_data[code]["mementos"] = 0
	


if __name__ == "__main__":
	post_data = read_csv()
	memento_data = read_mementos()
	combine(post_data, memento_data)


