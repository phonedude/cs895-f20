# save CDX response to file
import requests
import sys


filename = "katyperry_cdx.txt"

def get_urls():
	with open(sys.argv[1], "r") as f:
		urls = f.readlines()
		return urls


def get_cdx(urir):
	#urir = "https://www.instagram.com/p/CFchLF3nlf5/"
	req = "http://web.archive.org/cdx/search/cdx?url=" + urir + "&matchType=prefix"
	response = requests.get(req)

	if response.status_code != 200:
	  print (response.headers)
	else:
	  f = open (filename, "a")
	  f.write(response.text)
	  f.close()


def read_cdx():
	#How Many 200s
	f = open(filename, "r")
	lines = f.readlines()
	print("{} lines in CDX".format(len(lines)))	  
	cdx_200 = []
	for line in lines:
	  cols = line.split()
	  status = cols[4]
	  if (status == "200"):
	    cdx_200.append(line)
	print ("{} HTTP 200 lines in CDX".format(len(cdx_200)))
	return cdx_200


def SURT_urir(cdx_200):
	surt_list = ""
	#for i in range(30000):
	for i in cdx_200:
		cols = i.split()
		#cols = cdx_200[i].split()
		surt = cols[0]
		if surt != "com,instagram)/": 
			print(surt)
			surt_list = surt + "\n" + surt_list
	#print(surt_list)
	# filename = "katyperry_surt.txt"
	# g = open (filename, "w")
	# g.write(surt_list)
	# g.close()	


if __name__ == "__main__":
	# urls = get_urls()
	# for urir in urls:
	# 	cdx =  get_cdx(urir)
	# cdx_200 = read_cdx()
	SURT_urir(cdx_200)


"""
Katy perry's posts - 1643

For each url:
	get cdx
		- analyze
			url vs  number of mementos
			their status code
		- get urls + parameters
	initial url+ url's with parameters: check in other archives
"""

shortcode - mementos - date - likes

