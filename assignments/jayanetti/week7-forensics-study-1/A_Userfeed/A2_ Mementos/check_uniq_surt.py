import requests
import sys



def mementos(unique_surt):
	uniq_surt_multi = []
	for line in unique_surt:
	  if line.split()[0] != "1":
	    uniq_surt_multi.append(line)
	print(len(uniq_surt_multi))
	for i in range(len(uniq_surt_multi)):
	  print (uniq_surt_multi[i])

	# f = open(filename, "r")
	# lines = f.readlines()
	# print("{} lines in CDX".format(len(lines)))	  
	# cdx_200 = []
	# for line in lines:
	#   cols = line.split()
	#   status = cols[4]
	#   if (status == "200"):
	#     cdx_200.append(line)
	# print ("{} HTTP 200 lines in CDX".format(len(cdx_200)))
	# return cdx_200


def SURT_urir(cdx_200):
	surt_list = ""
	#for i in range(30000):
	for i in cdx_200:
	  cols = i.split()
	#  cols = cdx_200[i].split()
	  surt = cols[0]
	  if surt != "com,instagram)/": 
	    surt_list = surt + "\n" + surt_list
	#print(surt_list)
	filename = "instagram_surt.txt"
	f = open (filename, "w")
	f.write(surt_list)
	f.close()	


if __name__ == "__main__":
	with open(sys.argv[1], "r") as f:
		unique_surt = f.readlines()
	mementos(unique_surt)


