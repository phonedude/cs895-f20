import click
from Scraper import ArchiveBlogScraper
"""
archive_scrape.py
James Ecker

Driver for running a scrape on archives

"""

@click.command()
@click.option(
    '--in-file',
    default='news.txt'
)
@click.option(
    '--out-file',
    default='archived_news_posts.csv'
)
@click.option(
    '--category',
    type=click.Choice(['news', 'missionary'], case_sensitive=True),
    default='None'
)
def main(in_file: str, out_file: str, category: str) -> None:
    """
    Click command handle passing cli arguments to ArchiveBlogScraper constructor
    Runs scrape on the archive data specified by the user

    :param str in_file: uri for input file
    :param str out_file: uri for output csv file
    :param str category: news|missionary choice for blog category
    :return: None
    """
    scraper = ArchiveBlogScraper(in_file, out_file, category)
    scraper.run()


if __name__ == '__main__':
    main()
