import click
from Scraper import LiveScraper
"""
full_live_news_scrape.py
James Ecker

Driver for running a scrape on blog posts from the live web
**Currently requires saved HTML file from live web**

"""

@click.command()
@click.option(
    '--in-file',
    default='full_news_list.txt',
    help='Specify input file'
)
@click.option(
    '--out-file',
    default='full_live_news_posts.csv',
    help='Specify an output file'
)
@click.option(
    '--create-list',
    is_flag=True,
    default=False,
    help='Create a new list of posts from html file'
)
@click.option(
    '--html-file',
    default='sources/full_news.html',
    help='HTML file path'
)
def full_live_scrape(in_file: str, out_file: str, create_list: bool, html_file: str) -> None:
    """
    Click command handle passing cli arguments to LiveScraper constructor
    Runs scrape on the archive data specified by the user

    :param str in_file: uri for the input file
    :param str out_file: uri for the output csv
    :param bool create_list: specify whether to create a new list of blog posts in **sources/** directory
        **NOTE** create_list requires an HTML file for the live web in **sources/** directory
    :param str html_file: uri for the HTML file for the live web
    :return: None
    """
    scraper = LiveScraper(in_file, out_file, create_list, html_file)
    scraper.run()


if __name__ == "__main__":
    full_live_scrape()