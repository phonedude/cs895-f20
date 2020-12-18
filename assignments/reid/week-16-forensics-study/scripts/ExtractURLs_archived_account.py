import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import parse_qs

from selenium.common.exceptions import StaleElementReferenceException

# Getting href links: https://stackoverflow.com/questions/34759787/fetch-all-href-link-using-selenium-in-python
videoSectionUriRFile = open("videoSection_URI-Rs.txt", 'r')
videoSectionUriRList = []
videoSectionUriMList = []
for uri_r in videoSectionUriRFile:
    videoSectionUriRList.append(uri_r)
    videoSectionReq = requests.get("https://memgator.cs.odu.edu/timemap/link/" + str(uri_r).strip())
    ##similar to Memgator link file except it is a list of lines that would be in that file
    memgatorLinesList = videoSectionReq.text.split('\n')
    for line in memgatorLinesList:
        memgatorFields = line.split(';')
        if (len(memgatorFields) > 1) and ("memento" in str(memgatorFields[1]).lower()):
            #The URL is a URI-M for the video section
            uri_m = memgatorFields[0].replace('<', '').replace('>', '')
            videoSectionUriMList.append(uri_m)

# Getting the known videos from the live account
liveAccountVideosFile = open("known_video_URLs.txt", 'r')
knownVideoValues = []
for line in liveAccountVideosFile:
    if line.strip() != "":
        videoValue = parse_qs(urlparse.urlparse(line).query)['v'][0].strip()
        knownVideoValues.append(videoValue)

# Get the checkpoint from the previous execution of this program
checkpointFileName = "checkpoint_ExtractVideoURI-Rs.txt"
numberOfVideoSections = len(videoSectionUriMList)
checkpoint = 0
videoUriRList = []
with open(checkpointFileName, 'r') as c:
    checkpoint = int(c.readline().strip())
    if (checkpoint > 0) and (checkpoint <= numberOfVideoSections):
        choice = input("Resume from last checkpoint (" + str(checkpoint) + "/" + str(numberOfVideoSections) + ")? Y/n ")
        if "n" in choice.lower():
            #Overwrite files
            checkpoint = 0 
            privatedVideoUriRFile = open("privated_videos_Uri-Rs.txt", 'w')
            slowLoadingWebpageFile = open("Slow_Loading_Webpages.txt", 'w')
        else:
            #Append to the files: https://www.geeksforgeeks.org/reading-writing-text-files-python/
            privatedVideoUriRFile = open("privated_videos_Uri-Rs.txt", 'a')
            slowLoadingWebpageFile = open("Slow_Loading_Webpages.txt", 'a')
            
            # Read in the known values
            for uri_r in open("privated_videos_Uri-Rs.txt", 'r'):
                uri_r = uri_r.strip()
                videoUriRList.append(uri_r)
                videoValue = parse_qs(urlparse.urlparse(uri_r).query)['v'][0]
                knownVideoValues.append(videoValue)

iterations = 0
# For testing other archives # 
## videoSectionUriMList = ["http://wayback.vefsafn.is/wayback/20151019212412/https://www.youtube.com/user/JennaMarbles/videos", "https://swap.stanford.edu/20140514184439/http://www.youtube.com/user/JennaMarbles/videos","https://swap.stanford.edu/20140511232016/https://www.youtube.com/user/JennaMarbles/videos", "https://swap.stanford.edu/20131112031953/http://www.youtube.com/user/JennaMarbles/videos", "https://www.webarchive.org.uk/wayback/archive/20121021235939mp_/http://www.youtube.com/user/JennaMarbles/videos", "http://archive.md/20130701013638/https://www.youtube.com/user/JennaMarbles/videos", "https://web.archive.org/web/20140109102809/http://www.youtube.com/user/JennaMarbles/videos", "https://wayback.archive-it.org/all/20140228092724/http://www.youtube.com/user/JennaMarbles/videos", "http://archive.md/20140115172649/https://www.youtube.com/user/JennaMarbles/videos"]#Testing
for videoSectionUriM in videoSectionUriMList:
    if iterations < checkpoint:
        iterations = iterations + 1
        continue
    
    print("\n\n(" + str(iterations + 1) + "/" + str(numberOfVideoSections) + ")")
    print(videoSectionUriM)
    
    #Determine the type of web archive
    category = "other"
    #"""
    if "web.archive.org" in str(videoSectionUriM):
        category = "Internet Archive"
        crawlDateOld = videoSectionUriM.split("/http")[0].split('/')[-1].lower()
        crawlDateNew = crawlDateOld
        if "if_" in str(crawlDateNew):
            crawlDateNew = crawlDateNew.replace("if_", "id_")
        elif not("id_" in str(crawlDateNew)):
            crawlDateNew = crawlDateNew + "id_"
        videoSectionUriM = videoSectionUriM.replace(crawlDateOld, crawlDateNew)
    elif "wayback.archive-it.org" in str(videoSectionUriM):
        category = "Archive-It"
    elif "//archive." in str(videoSectionUriM):
        category = "archive.today"
    elif "www.webarchive.org.uk" in str(videoSectionUriM):
        category = "UK Web Archive"
        continue # Can only be accessed on site
    elif "swap.stanford.edu" in str(videoSectionUriM):
        category = "Stanford Web Archive"
    elif ".vefsafn." in str(videoSectionUriM):
        category = "Icelandic Web Archive"
    else:
        category = "other"
    #"""
    
    # Get links from the current video section
    driver = webdriver.Chrome('.\ChromeDrivers\chromedriver_win32\chromedriver.exe')
    driver.get(videoSectionUriM)
    sleep(2)
    try:
        #Check to see if any elements are stale
        linkElements = driver.find_elements_by_xpath("//a[@href]")
        for le in linkElements:
            le.get_attribute("href")
    except StaleElementReferenceException:
        # When the elments are stale, need to restart the web page
        #print("Slower than usual Webpage: " + videoSectionUriM)
        sleep(120)
        try:
            linkElements = driver.find_elements_by_xpath("//a[@href]")
            for le in linkElements:
                le.get_attribute("href")
        except StaleElementReferenceException:
            driver.quit()
            print("Slow Loading Webpage: " + videoSectionUriM, file=slowLoadingWebpageFile)
            continue
    
    previousVideoValue = ""
    videoValue = ""
    for le in linkElements:
        if "watch?v=" in le.get_attribute("href").lower():            
            # Extract parameter from URL: https://stackoverflow.com/questions/5074803/retrieving-parameters-from-a-url
            # check to see if the video URL is unique and has not been seen before
            videoValue = parse_qs(urlparse.urlparse(le.get_attribute("href")).query)['v'][0].strip()
            if (previousVideoValue != videoValue) and (not(videoValue in knownVideoValues)):
                videoParam = "v=" + videoValue
                currentUriR = "https://www.youtube.com/" + le.get_attribute("href").split('/')[-1].split('?')[0] + '?' + videoParam
                videoUriRList.append(currentUriR)
                knownVideoValues.append(videoValue)
                print("Found Privated Video: " + str(currentUriR))
                #print(category + ": " + str(currentUriR), file=privatedVideoUriRFile)
                print(str(currentUriR), file=privatedVideoUriRFile)
            previousVideoValue = videoValue
            
            """
            #older way of checking for a unique video value and adding to the videoUriRList
            if len(videoUriRList) > 0 and videoUriRList[-1] != currentUriR:
                if not(currentUriR in videoUriRList):
                    videoUriRList.append(currentUriR)
                    print(str(currentUriR))
            elif len(videoUriRList) == 0:
                videoUriRList.append(currentUriR)
            """
            
            """ Not needed. Memgator should be able to get most of the mementos
            if "id_/" in videoSectionUriM:
                currentUriM = videoSectionUriM.split("id_/")[0] + "/" + currentUriR            
                if len(foundUriMList) > 0 and foundUriMList[-1] != currentUriM:
                    foundUriMList.append(currentUriM)
                elif len(foundUriMList) == 0:
                    foundUriMList.append(currentUriM)
            """

    driver.quit()
    print("Current Total Privated Videos: " + str(len(videoUriRList)))
    
    iterations = iterations + 1
    with open(checkpointFileName, 'w') as c:
        c.write(str(iterations))

#end loop

print("\n\n All Privated Videos:")
for uri in videoUriRList:
    print(uri)

print("Final Total Privated Videos: " + str(len(videoUriRList)))

#Getting URI-Ms from MemGator
## Determine URI-Ms from Internet Archive's web archive, but for the rest use Memgator to get
## URI-Ms.
"""
reqs = requests.get("https://memgator.cs.odu.edu/timemap/link/https://www.youtube.com/watch?v=jWAWc9_21J0")

##similar to Memgator link file except it is a list of lines that would be in that file
reqs.text.split('\n')
    
"""
 

