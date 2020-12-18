import requests
import os
from time import sleep
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import parse_qs
#*** This program requires the web page to be scrolled by the user so that it can extract all of the URLs
## Update secondsToSleep if the amount of time to scroll takes longer than 20 seconds.
secondsToSleep = 20


# Getting href links: https://stackoverflow.com/questions/34759787/fetch-all-href-link-using-selenium-in-python
searchURLList = ["https://www.youtube.com/user/JennaMarbles/videos"]

foundUriRList = []
for url in searchURLList:
    driver = webdriver.Chrome('.\ChromeDrivers\chromedriver_win32\chromedriver.exe')
    driver.get(url)

    sleep(secondsToSleep)

    linkElements = driver.find_elements_by_xpath("//a[@href]")
    for le in linkElements:
        if "watch?v=" in le.get_attribute("href").lower():
            #print(le.get_attribute("href"))
            
            # Extract parameter from URL: https://stackoverflow.com/questions/5074803/retrieving-parameters-from-a-url
            videoParam = "v=" + parse_qs(urlparse.urlparse(le.get_attribute("href")).query)['v'][0]
            currentUriR = "https://www.youtube.com/" + le.get_attribute("href").split('/')[-1].split('?')[0] + '?' + videoParam
            if len(foundUriRList) > 0 and foundUriRList[-1] != currentUriR:
                foundUriRList.append(currentUriR)
            elif len(foundUriRList) == 0:
                foundUriRList.append(currentUriR)

    driver.quit()

#end loop

print("\n\nURI-Rs:")
knownVideoURLFile = open("known_video_URLs.txt", 'wt')
for uri in foundUriRList:
    print(uri)
    print(uri, file=knownVideoURLFile)
    

print("Number of videos: " + str(len(foundUriRList)))
driver.quit()
 

