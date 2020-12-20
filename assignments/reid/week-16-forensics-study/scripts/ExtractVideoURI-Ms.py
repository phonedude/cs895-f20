import requests
import os
from time import sleep
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import parse_qs

from selenium.common.exceptions import StaleElementReferenceException

videoUriRFile = open("privated_videos_Uri-Rs.txt", 'r')
videoUriMFile = open("privated_videos_Uri-Ms.txt", 'w')
videoUriMFile_categorized = open("categorized_privated_videos_Uri-Ms.txt", 'w')
videoUriMFile_categorized_1to100 = open("1-100_privated_videos_Uri-Ms.txt", 'w')
videoUriMFile_categorized_101to200 = open("101-200_privated_videos_Uri-Ms.txt", 'w')
videoUriMFile_categorized_201to300 = open("201-300_privated_videos_Uri-Ms.txt", 'w')
videoUriRList = []
videoUriMList = []
counter = 0
for uri_r in videoUriRFile:
    uri_r = uri_r.strip()
    videoUriRList.append(uri_r)
    print(uri_r.strip(), file=videoUriMFile_categorized)
    if counter < 100:
        print("Video " + str(counter+1) +": " + uri_r.strip(), file=videoUriMFile_categorized_1to100)
    elif counter < 200:
        print("Video " + str(counter+1) +": " + uri_r.strip(), file=videoUriMFile_categorized_101to200)
    elif counter < 300:
        print("Video " + str(counter+1) +": " + uri_r.strip(), file=videoUriMFile_categorized_201to300)
    #print(videoUriRList[-1])
    videoReq = requests.get("https://memgator.cs.odu.edu/timemap/link/" + str(uri_r).strip())
    ##similar to Memgator link file except it is a list of lines that would be in that file
    memgatorLinesList = videoReq.text.split('\n')
    for line in memgatorLinesList:
        memgatorFields = line.split(';')
        if (len(memgatorFields) > 1) and ("memento" in str(memgatorFields[1]).lower()):
            #The URL is a URI-M for the video section
            uri_m = memgatorFields[0].replace('<', '').replace('>', '').strip()
            videoUriMList.append(uri_m)
            print(uri_m, file=videoUriMFile)
            print("\t" + str(uri_m), file=videoUriMFile_categorized)
            if counter < 100:
                print("\t" + str(uri_m), file=videoUriMFile_categorized_1to100)
            elif counter < 200:
                print("\t" + str(uri_m), file=videoUriMFile_categorized_101to200)
            elif counter < 300:
                print("\t" + str(uri_m), file=videoUriMFile_categorized_201to300)

    print("\n\n", file=videoUriMFile_categorized)
    if counter < 100:
        print("\n\n", file=videoUriMFile_categorized_1to100)
    elif counter < 200:
        print("\n\n", file=videoUriMFile_categorized_101to200)
    elif counter < 300:
        print("\n\n", file=videoUriMFile_categorized_201to300)
    
    counter = counter + 1
    print("(" + str(counter)+ "/262)")