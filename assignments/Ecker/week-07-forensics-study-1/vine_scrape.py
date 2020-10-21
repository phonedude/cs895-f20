import click
from Scraper import VineScraper
"""
vine_scrape.py
James Ecker

Driver for running a scrape on archived issues of Vine and Branches magazine
"""

@click.command()
@click.option(
    '--in-file',
    default='vine.txt'
)
@click.option(
    '--out-file',
    default='archived_vine_issues.csv'
)
@click.option(
    '--find-missing',
    is_flag=True,
    default=False
)
@click.option(
    '--download',
    is_flag=True,
    default=False
)
def scrape_vine(in_file: str, out_file: str, find_missing: bool, download: bool) -> None:
    """
    Click command handle passing cli arguments to VineScraper constructor
    Runs scrape on the archive data specified by the user

    :param str in_file: uri for input file
    :param str out_file: uri for output csv file
    :param bool find_missing: specify whether to track issues missing since last memento
    :param bool download: specify whether to download issues **WARNING** this will take a **LONG** time
    :return: None
    """
    scraper = VineScraper(in_file, out_file, find_missing, download)
    scraper.run()


if __name__ == "__main__":
    scrape_vine()