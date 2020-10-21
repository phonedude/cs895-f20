from abc import ABC, abstractmethod
import re
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


class Scraper(ABC):
    """
    Scraper

    Abstract class for Scraper classes
    Specifies run() and parse_soup() methods as required abstractmethods


    **Instance Variables**
    in_file: str
    data: List[Any]
    columns: List[Any]
    """
    def __init__(self, in_file: str) -> None:
        """
        Scraper constructor

        :param str in_file: uri for input file
        :rtype: None
        """

        self.in_file = 'sources/{}'.format(in_file)
        self.data = []
        self.columns = []
        super().__init__()

    @abstractmethod
    def run(self) -> None:
        """
        run()
        abstractmethod to require descendent classes to implement
        :rtype: None
        """
        pass

    @abstractmethod
    def parse_soup(self, soup: BeautifulSoup, prepend: list = None) -> list:
        """
        parse_soup()
        abstractmethod to require descendent classes to implement

        :param BeautifulSoup soup: soup representation of DOM under inspection
        :param list prepend: any data to prepend to return list
        :return: list containing the data collected
        :rtype: list
        """
        pass

    @staticmethod
    def read_file(in_file: str) -> list:
        """
        read_file()
        reads the file specified by @in_file

        :param str in_file: uri for the input file
        :return: list containing all of the lines in the input file
        :rtype: list
        """
        print('Reading from {}'.format(in_file))
        with open(in_file, "r") as fp:
            lines = fp.readlines()
        return lines

    def create_dataframe(self) -> pd.DataFrame:
        """
        create_dataframe()
        creates a Pandas Dataframe from the data in Scraper.data

        :return: a Pandas.Dataframe containing the data in Scraper.data
        :rtype: Pandas.DataFrame
        """
        df = pd.DataFrame(self.data, columns=self.columns)
        return df

    def save_to_csv(self, outfile: str, msg=None) -> None:
        """
        save_to_csv()
        saves scraped data to a csv file

        :param str outfile: uri for the resulting csv
        :param str msg: string for specifying a custom message to be sent to terminal when calling this function
        :rtype: None
        """
        if not os.path.exists("dataset/"):
            print('Creating dataset/ directory')
            os.mkdir("dataset/")
        outfile = "dataset/{}".format(outfile)
        if not msg:
            print('Saving scrape as {}'.format(outfile))
        else:
            print(msg)
        self.create_dataframe().to_csv(outfile, index=False)


class ArchiveBlogScraper(Scraper):
    """
    ArchiveBlogScraper
    Scraper for scraping archives

    **Instance Variables**
    in_file: str: uri for input file
    out_file: str: uri for the resulting csv
    category: str: news|missionary choice for blog category
    columns: List[str]: list containing header descriptions
    """

    def __init__(self, in_file: str, out_file: str, category: str) -> None:
        """
        ArchiveBlogScraper constructor

        :param str in_file: uri for input file
        :param str out_file: uri for output csv file
        :param str category: news|missionary choice for blog category
        :rtype: None
        """
        super().__init__(in_file)
        self.columns = ["memento_time", "original_url", "post_id", "date", "title", "entry"]
        self.out_file = out_file
        self.category = category

    def run(self) -> None:
        """
        run()
        Handles collecting data

        :return: None
        """
        print('Scraping archives for all {} posts'.format(self.category))
        lines = self.read_file(self.in_file)
        lines = self.filter(lines)
        for line in tqdm(lines):
            if re.search(r"\?p=", line):
                line = line.strip()
                page = requests.get(line)
                memento_time = line.split('/web/')[1].split('/http')[0]
                original_uri = line.split(memento_time + '/')[1]
                post_id = original_uri.split("p=")[1]
                soup = BeautifulSoup(page.content, 'html.parser')
                self.data.append(self.parse_soup(soup, [memento_time, original_uri, post_id]))
        self.save_to_csv('archived_{}_blog_posts.csv'.format(self.category) if self.category else self.out_file )

    def parse_soup(self, soup: BeautifulSoup, prepend: list = None) -> list:
        """
        parse_soup()
        Parses the DOM for the data under inspection and collects data

        :param BeautifulSoup soup: representation of DOM under inspection
        :param list prepend: scraped data will be appended to this list
        :return: list containing data for blog post
        :rtype: list
        """
        if soup.find("div", {"class": "entry_date"}):
            date = soup.find("div", {"class": "entry_date"}).attrs['title'].replace("\n", " ").strip().replace(",",
                                                                                                               "")
        elif soup.find("div", class_="post"):
            date = soup.find("div", class_="post").p.get_text().split("|")[0].strip().replace("\n",
                                                                                              " ").strip().replace(
                ",", "")
            if date is None:
                date = ""
        else:
            date = ""
        if soup.find("div", id="post_header"):
            title = soup.find("div", id="post_header").a.get_text().replace("\n", " ").strip().replace(",", "")
        elif soup.find("div", class_="post"):
            title = soup.find("div", class_="post").a.attrs['title'].replace("\n", " ").strip().replace(",", "")
            if title is None:
                title = ""
        else:
            title = ""
        if soup.find("div", {"class": "entry_content"}):
            entry = soup.find("div", {"class": "entry_content"}).get_text().replace("\n", " ").strip().replace(",",
                                                                                                               "")
        elif soup.find("div", {"class": "entry"}):
            entry = soup.find("div", {"class": "entry"}).get_text().replace("\n", " ").strip().replace(",", "")
        else:
            entry = ""
        return prepend + [date, title, entry] if prepend else [date, title, entry]

    @staticmethod
    def filter(lines: list) -> list:
        """
        filter()
        Filters out any lines not containing a blog post

        :param list lines: List of lines from input file
        :return: list containing filtered uris
        :rtype: list
        """
        found = []
        for line in lines:
            if re.search(r"\?p=", line):
                found.append(line)
        return found


class VineScraper(Scraper):
    """
    VineScraper
    Scraper to scrape metadata (and, optionally, download) for issues of Vine and Branches magazine in the archives

    **Instance Variables**
    out_file: str: uri for output csv
    find_missing: bool: specify whether to track issues missing since last memento
    memento_now: List[Any]: list containing issues found in the current memento
    missing: List[Any]: list containing any missing issues found in processing
    download: bool: specify whether to download issues ::WARNING:: this will take a ::LONG:: time
    memento_time: str: memento time for the memento currently being processed
    columns: List[str]: list containing descriptions for column headers
    """

    def __init__(self, in_file: str, out_file: str, find_missing: bool, download: bool) -> None:
        """
        VineScraper constructor

        :param str in_file: uri for input file
        :param str out_file: uri for output csv file
        :param bool find_missing: specify whether to track issues missing since last memento
        :param bool download: specify whether to download issues **WARNING** this will take a **LONG** time
        :rtype: None
        """
        super().__init__(in_file)
        self.out_file = out_file
        self.find_missing = find_missing
        if self.find_missing:
            self.memento_now = []
            self.missing = []
        self.download = download
        self.memento_time = ''
        self.columns = ["memento_time", "file_name", "URI"]

    def run(self) -> None:
        """
        run()
        Handles collecting data

        :rtype: None
        """
        print("Scraping metadata{} for all archived issues of Vine and Branches magazine".format(
            ' and downloading all files' if self.download else ''))
        lines = self.read_file(self.in_file)
        for line in tqdm(lines):
            page = requests.get(line)
            self.memento_time = line.split('/web/')[1].split('/http')[0]
            if self.find_missing:
                memento_last = self.memento_now
                self.memento_now = []
            soup = BeautifulSoup(page.content, 'html.parser')
            issues = self.parse_soup(soup)
            for issue in issues:
                self.data.append(issue)
            if self.find_missing:
                missing_from_last = self.diff(memento_last, self.memento_now)
                if missing_from_last:
                    self.missing.append([self.memento_time, missing_from_last])
        self.save_to_csv(self.out_file)
        if self.find_missing:
            df = pd.DataFrame(self.missing, columns=["memento_time", "missing"])
            print('Saving missing issues found in dataset/missing.csv')
            df.to_csv('dataset/missing.csv', index=False)

    def parse_soup(self, soup: BeautifulSoup, prepend: list = None, ) -> list:
        """
        parse_soup()
        Parses the DOM for the data under inspection and collects data

        :param BeautifulSoup soup: representation of DOM under inspection
        :param list prepend: scraped data will be appended to this list
        :return: list containing the metadata for the issues in this memento
        :rtype: list
        """
        issue_list = []
        issues = soup.findAll("a", href=True)
        for issue in issues:
            if os.path.splitext(issue['href'])[1] in ['.pdf']:
                base_uri = 'https://web.archive.org'
                if "issues" in issue['href']:
                    base_uri = "{}/web/{}/http://www.peopleofpraise.org/thevine/".format(base_uri, self.memento_time)
                uri = "{}{}".format(base_uri, issue['href'])
                if self.download:
                    self.download_issue(uri, self.memento_time)
                issue_list.append([self.memento_time, os.path.basename(uri), uri])
                if self.find_missing:
                    self.memento_now.append(os.path.basename(uri))
        return issue_list

    @staticmethod
    def diff(memento_last: list, memento_now: list) -> list:
        """
        diff()
        Finds the elements missing in memento_now since memento_last

        :param list memento_last: list of issues found in the last memento
        :param list memento_now: list of issues found in the current memento
        :return: list containing all of the issues missing in this memento since the last memento
        :rtype: list
        """
        set1 = set(memento_last)
        set2 = set(memento_now)
        return list(sorted(set1 - set2))

    @staticmethod
    def download_issue(uri: str, memento_time: str) -> None:
        """
        download_issue()
        Downloads the issue specified by the uri and memento_time and saves them under the **vine/** directory.

        The **vine/** directory is organized by memento_time

        :param str uri: uri for issue's pdf file
        :param str memento_time: the memento time for the pdf file in the archives
        :rtype: None
        """
        if not os.path.exists("vine/{}".format(memento_time)):
            os.mkdir("vine/{}".format(memento_time))
        with open("vine/{}/{}".format(memento_time, os.path.basename(uri)), 'wb') as fd:
            fd.write(requests.get(uri).content)


class LiveScraper(Scraper):
    """
    LiveScraper
    Scraper for scraping blog posts from the live web

    **Instance Variables**
    out_file: str
    create_list: bool
    html_file: str
    columns: List[str]
    """

    def __init__(self, in_file: str, out_file: str, create_list: bool, html_file: str) -> None:
        """
        LiveScraper constructor

        :param str in_file: uri for the input file
        :param str out_file: uri for the output csv
        :param bool create_list: specify whether to create a new list of blog posts in **sources/** directory
            **NOTE** create_list requires an HTML file for the live web in **sources/** directory
        :param str html_file: uri for the HTML file for the live web
        :rtype: None
        """
        super().__init__(in_file)
        self.out_file = out_file
        self.create_list = create_list
        self.html_file = html_file
        self.columns = ["post_id", "date", "title", "entry", "uri"]

    def run(self) -> None:
        """
        run()
        Handles collecting data

        :rtype: None
        """
        if self.create_list:
            in_file = self.get_all_posts()
        else:
            in_file = self.in_file
        lines = self.read_file(in_file)
        for line in tqdm(lines):
            post = self.get_post(line)
            self.data.append(post)
        self.save_to_csv(self.out_file)

    def parse_soup(self, soup: BeautifulSoup, prepend: list = None) -> list:
        """
        parse_soup()
        Parses the DOM for the data under inspection and collects data

        :param BeautifulSoup soup: representation of DOM under inspection
        :param list prepend: scraped data will be appended to this list
        :return: list containing the collected data
        :rtype: list
        """
        title = soup.find("div", id="post_header").a.get_text().replace("\n", " ").strip().replace(",", "")
        date = soup.find("div", {"class": "entry_date"}).attrs['title'].replace("\n", " ").strip().replace(",", "")
        entry = soup.find("div", {"class": "entry_content"}).get_text().replace("\n", " ").strip().replace(",", "")
        return prepend + [date, title, entry] if prepend else [date, title, entry]

    def get_post(self, line: str) -> list:
        """
        get_post()
        Retrieves a post by its post_id

        :param str line: line should be a uri to the post, containing a '?=p'
        :return: list containing blog post data
        :rtype: list
        """
        line = line.strip()
        page = requests.get(line)
        post_id = line.split("p=")[1]
        soup = BeautifulSoup(page.content, 'html.parser')
        post = self.parse_soup(soup, [post_id])
        return post + [line]

    def get_all_posts(self) -> str:
        """
        get_all_posts()
        Traverses over the DOM for the LiveScraper.html_file and pulls links to each blog post

        :return: uri for the list that was created
        :rtype: str
        """
        print('Getting all live posts from {}'.format(self.in_file))
        soup = BeautifulSoup(open(self.html_file), "html.parser")
        out_file = 'full_news_list.txt'
        for a in soup.select('.post_block .text .excerpt .more a'):
            with open('sources/{}'.format(out_file), 'a+') as fp:
                fp.write('{}\n'.format(a['href']))
        return out_file
