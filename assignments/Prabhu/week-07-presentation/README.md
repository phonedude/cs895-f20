## Student Forensics Study - 1

### Topic

Amy Barrett - Link to People of Praise

### Presentation

Google Sheets - [https://docs.google.com/presentation/d/1PXl4V0goVzvXQ6fhmxRSechoPFgZW28skF_4W3pDzxA/edit?usp=sharing](https://docs.google.com/presentation/d/1PXl4V0goVzvXQ6fhmxRSechoPFgZW28skF_4W3pDzxA/edit?usp=sharing)


### Data

#### Reference count for live pages

Data source - [CSV](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/data/LivePages.csv) / [XLSX](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/data/LivePages.xlsx)

Summary - CSV or XLSX file containing the count of mentions of Amy Barrett and her family in each page on the live website http://www.peopleofpraise.org that contain one of the keyword - "Amy", "Barrett" or "Coney"

#### Reference count for archived pages

Data source - [CSV](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/data/ArchivedPages.csv) / [XLSX](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/data/ArchivedPages.xlsx)

Summary - CSV or XLSX file containing the count of mentions of Amy Barrett and her family in the pdf documents that were deleted from the website http://www.peopleofpraise.org. The PDFs were retrieved through the [Internet Archive](http://web.archive.org/)

**Please note that the count of mentions were manually compiled**

### Scripts

#### Get Followers

Source - [getFollowers.py](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/scripts/getFollowers.py)

Summary - Python script which uses the library Tweepy to retrive the twitter usernames of users that are following a certain account

#### Get Tweets

Source - [getTweets.py](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/scripts/getTweets.py)

Summary - Python script which uses the library Tweepy to retrive the tweets of a list of users.

#### Check Inactive

Source - [checkInactive.py](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/scripts/checkInactive.py)

Summary - Python script which uses the library requests to check if a list of urls are still active or not.

#### Sanitize

Source - [sanitize.py](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/scripts/sanitize.py)

Summary - Python script which sanitizes a list of urls so that they are in a standard format.

#### Match Web Content

Source - [matchWebContent.py](https://raw.githubusercontent.com/phonedude/cs895-f20/master/assignments/Prabhu/week-07-presentation/scripts/matchWebContent.py)

Summary - Python script which craws a list of urls and checks if the html content of the url matches a given regular expression.





