# Forensics Study 1 - peopleofpraise.org
James Ecker

![Big Picture](images/bigpicture.png)

The code and data in this project were used to analyze the alleged scrubbing of data from http://peopleofpraise.org pertaining to Amy Coney Barrett and her family

Slides associated with this project are available on [Google Slides](https://drive.google.com/file/d/1fL9TBw0gtuGNwSGKMDgBU6XT2GVWm7it/view?usp=sharing) and in this repo as a Power Point presentation named [`Jim Ecker Forensics Study 1.pptx`](https://github.com/jim-ecker/cs895-f20/blob/master/assignments/Ecker/week-07-forensics-study-1/Jim%20Ecker%20Forensics%20Study%201.pptx)
# Requirements
python 3

Create a python 3 virtual environment and install the following python modules

`pip install requests bs4 pandas tqdm click` 

You can run the following scrapes:

#### Live News Blog Posts

This script will pull all of the news blog post links from `sources/full_news.html` and create a list of the found urls in `sources/full_news_list.txt`. `sources/full_news_list.txt` is included in this repo

`python full_live_news_scrape.py`

If you do not have a list of urls in `sources/`, you'https://github.com/jim-ecker/cs895-f20/blob/master/assignments/Ecker/week-07-forensics-study-1/Jim%20Ecker%20Forensics%20Study%201.pptxhttps://github.com/jim-ecker/cs895-f20/blob/master/assignments/Ecker/week-07-forensics-study-1/Jim%20Ecker%20Forensics%20Study%201.pptxll need to run this script with the `--create-list` flag.

`python full_live_news_scrape.py --create-list`

Running a scrape with the `--create-list` flag requires a saved version of the http://peopleofpraise.org/news page with all of the blog post thumbnails loaded. I had to do this manually, but have included the html file at `sources/full_news.html`

#### Archived News Blog Posts

This script runs a scrape on news blog posts in the Internet Archives.

To run the script, you need a list of news blog urls (this is already included in the repo at `sources/news.txt`. 

However, if it isn't there you can get one by performing a prefix CDX query searching for http://peopleofpraise.org/news

The following curl command will perform this CDX query, return a list of found mementos, and write it to `sources/news.txt`

`curl -s "http://web.archive.org/cdx/search/cdx?url=peopleofpraise.org/news&matchType=prefix" | sort -k 2 | awk '{print "https://web.archive.org/web/" $2 "/" $3}; > sources/news.txt'
`

Once you have the uri list in `sources/` you can run the script 

`python archive-scrape.py`

#### Archived Missionary Blog Posts

You can also run a scrape on any missionary blog posts in the archives. A list of missionary blog post uris is already included in this repo at `sources/missionary.txt`.

`python archive-scrape.py --category missionary --in-file missionary.txt`

> *NOTE:* this script is kind of clunky when running it for missionary posts. You have to explicitly declare the name of the input file. 

> *NOTE:* the file does not include the `sources/` directory when specifying it by cli flag, it is handled by the script.


However, if it isn't there you can create one by executing the following command:

`curl -s "http://web.archive.org/cdx/search/cdx?url=peopleofpraise.org/missionary&matchType=prefix" | sort -k 2 | awk '{print "https://web.archive.org/web/" $2 "/" $3};' > sources/missionary.txt`

#### Archived Issues of Vine and Branches Magazine

This script will scrape all issues of Vine and Branches Magazine. By default, it only scrapes metadata. There is an option to download the issues as well. However, this takes a *LONG* time (~20 hours when I ran it).

`python vine_scrape.py`

This repo already provides the required input file in `sources/vine.txt`. However, if it isn't there you can generate a new one with the following command:

`curl -s "http://web.archive.org/cdx/search/cdx?url=peopleofpraise.org/thevine" | sort -k 2 | awk '{print "https://web.archive.org/web/" $2 "/" $3};' > sources/vine.txt
`

You can also track any missing issues as you are processing the scrape by including the `--find-missing` cli flag

`python vine_scrape.py --find-missing`

This will track any issues that go missing between mementos and save a .csv file describing them in `dataset/missing.csv`

# Datasets
Located in `dataset/`

## archived_missionary_blog_posts.csv
Describes each blog post found when scraping missionary blog posts in the archives with `../archive_scrape.py`

### Path

`dataset/archived_missionary_blog_posts.csv`

### Header

| memento_time | original_url | post_id | date | title | entry |
|--------------|--------------|---------|------|-------|-------|

## archived_news_blog_posts.csv
Describes each blog post found when scraping missionary blog posts in the archives with `../archive_scrape.py`

### Path

`dataset/archived_news_blog_posts.csv`

### Header
| memento_time | original_url | post_id | date | title | entry |
|--------------|--------------|---------|------|-------|-------|

## archived_vine_issues.csv
Describes each blog post found when scraping issues of Vine and Branches magazine with `../vine_scrape.py`

### Path

`dataset/archived_vine_issues.csv`

### Header
| memento_time | file_name | uri 
|--------------|--------------|---------|

## full_live_news_posts.csv
Describes each blog post found when scraping a copy of the live web peopleofpraise.org/news with `../full_live_news_scrape.py`

### Path

`dataset/full_live_news_posts.csv`

### Header

| post_id | date | title | entry | uri 
|--------------|--------------|---------|--------------|----------|

## missing.csv
Describes each issue of Vine and Branches magazine missing from a memento, since the last memento, when scraping issues with `../vine_scrape.py`

### Path

`dataset/missing.csv`

### Header

| memento_time | missing 
|--------------|--------------|


# Scraper module


### class Scraper.ArchiveBlogScraper(in_file: str, out_file: str, category: str)
Bases: `Scraper.Scraper`

Scraper for scraping archives

**Instance Variables**

* **in_file**: str: uri for input file

* **out_file**: str: uri for the resulting csv

* **category**: str: news|missionary choice for blog category

* **columns**: List[str]: list containing header descriptions


#### \__init__(in_file: str, out_file: str, category: str)
ArchiveBlogScraper constructor


* **Parameters**

    **in_file** (*str*) – uri for input file

    **out_file** (*str*) – uri for output csv file

    **category** (*str*) – news|missionary choice for blog category



* **Return type**

    None



#### static filter()
Filters out any lines not containing a blog post


* **Parameters**

    **lines** (*list*) – List of lines from input file



* **Returns**

    list containing filtered uris



* **Return type**

    list



#### parse_soup()
Parses the DOM for the data under inspection and collects data


* **Parameters**

    **soup** (*BeautifulSoup*) – representation of DOM under inspection

    **prepend** (*list*) – scraped data will be appended to this list



* **Returns**

    list containing data for blog post



* **Return type**

    list



#### run()
Handles collecting data


* **Returns**

    None



### class Scraper.LiveScraper(in_file: str, out_file: str, create_list: bool, html_file: str)
Bases: `Scraper.Scraper`

Scraper for scraping blog posts from the live web

**Instance Variables**

* **out_file**: str

* **create_list**: bool

* **html_file**: str

* **columns**: List[str]


#### \__init__(in_file: str, out_file: str, create_list: bool, html_file: str)
LiveScraper constructor


* **Parameters**

    **in_file** (*str*) – uri for the input file

    **out_file** (*str*) – uri for the output csv

    **create_list** (*bool*) – specify whether to create a new list of blog posts in **sources/** directory

    > **NOTE** create_list requires an HTML file for the live web in **sources/** directory

    **html_file** (*str*) – uri for the HTML file for the live web



* **Return type**

    None



#### get_all_posts()
Traverses over the DOM for the LiveScraper.html_file and pulls links to each blog post


* **Returns**

    uri for the list that was created



* **Return type**

    str



#### get_post()
Retrieves a post by its post_id


* **Parameters**

    **line** (*str*) – line should be a uri to the post, containing a ‘?=p’



* **Returns**

    list containing blog post data



* **Return type**

    list



#### parse_soup()
Parses the DOM for the data under inspection and collects data


* **Parameters**

    **soup** (*BeautifulSoup*) – representation of DOM under inspection

    **prepend** (*list*) – scraped data will be appended to this list



* **Returns**

    list containing the collected data



* **Return type**

    list



#### run()
Handles collecting data


* **Return type**

    None



### class Scraper.Scraper(in_file: str)
Bases: `abc.ABC`

Abstract class for Scraper classes
Specifies run() and parse_soup() methods as required abstractmethods

**Instance Variables**

* **in_file**: str

* **data**: List[Any]

* **columns**: List[Any]


#### \__init__(in_file: str)
Scraper constructor


* **Parameters**

    **in_file** (*str*) – uri for input file



* **Return type**

    None



#### create_dataframe()
creates a Pandas Dataframe from the data in Scraper.data


* **Returns**

    a Pandas.Dataframe containing the data in Scraper.data



* **Return type**

    Pandas.DataFrame



#### abstract parse_soup()
abstractmethod to require descendent classes to implement


* **Parameters**

    **soup** (*BeautifulSoup*) – soup representation of DOM under inspection

    **prepend** (*list*) – any data to prepend to return list



* **Returns**

    list containing the data collected



* **Return type**

    list



#### static read_file()
reads the file specified by @in_file


* **Parameters**

    **in_file** (*str*) – uri for the input file



* **Returns**

    list containing all of the lines in the input file



* **Return type**

    list



#### abstract run()
abstractmethod to require descendent classes to implement

* **Return Type** 

    None


#### save_to_csv()
saves scraped data to a csv file


* **Parameters**

    **outfile** (*str*) – uri for the resulting csv

    **msg** (*str*) – string for specifying a custom message to be sent to terminal when calling this function



* **Return type**

    None



### class Scraper.VineScraper(in_file: str, out_file: str, find_missing: bool, download: bool)
Bases: `Scraper.Scraper`

Scraper to scrape metadata (and, optionally, download) for issues of Vine and Branches magazine in the archives

**Instance Variables**

* **out_file**: str: uri for output csv

* **find_missing**: bool: specify whether to track issues missing since last memento

* **memento_now**: List[Any]: list containing issues found in the current memento

* **missing**: List[Any]: list containing any missing issues found in processing

* **download**: bool: specify whether to download issues ::WARNING:: this will take a ::LONG:: time

* **memento_time**: str: memento time for the memento currently being processed

* **columns**: List[str]: list containing descriptions for column headers


#### \__init__(in_file: str, out_file: str, find_missing: bool, download: bool)
VineScraper constructor


* **Parameters**

    **in_file** (*str*) – uri for input file

    **out_file** (*str*) – uri for output csv file

    **find_missing** (*bool*) – specify whether to track issues missing since last memento

    **download** (*bool*) – specify whether to download issues **WARNING** this will take a **LONG** time



* **Return type**

    None



#### static diff()
Finds the elements missing in memento_now since memento_last


* **Parameters**

    **memento_last** (*list*) – list of issues found in the last memento

    **memento_now** (*list*) – list of issues found in the current memento



* **Returns**

    list containing all of the issues missing in this memento since the last memento



* **Return type**

    list



#### static download_issue()
Downloads the issue specified by the uri and memento_time and saves them under the **vine/** directory.

The **vine/** directory is organized by memento_time


* **Parameters**

    **uri** (*str*) – uri for issue’s pdf file

    **memento_time** (*str*) – the memento time for the pdf file in the archives



* **Return type**

    None



#### parse_soup()
Parses the DOM for the data under inspection and collects data


* **Parameters**

    **soup** (*BeautifulSoup*) – representation of DOM under inspection

    **prepend** (*list*) – scraped data will be appended to this list



* **Returns**

    list containing the metadata for the issues in this memento



* **Return type**

    list



#### run()
Handles collecting data


* **Return type**

    None

