"""
Scrape data from an IMDB user's list.

In the current embodiment, we only support lists of movies.
"""

import csv
import re
from StringIO import StringIO
import urllib2
import urlparse


IMDB_URL_ROOT = 'http://www.imdb.com/'

IMDB_KEY_TITLE = 'Title'
IMDB_KEY_URL = 'URL'
IMDB_KEY_YEAR = 'Year'

LOCAL_KEY_TITLE = 'title'
LOCAL_KEY_URL = 'url'
LOCAL_KEY_YEAR = 'year'


def get_movie_items_from_list_url(list_url):
    """The main entry point method that gets the list of movie items
    from the given IMDB list url.

    Args:
        list_url: The full url of the list to parse.

    Returns:
        A list of dictionaries with keys:
             * title
             * url
             * year
    """
    list_page_html = urllib2.urlopen(list_url).read()
    export_csv_data = _parse_list_page_html(list_page_html)
    return _get_movie_items_from_csv_data(export_csv_data)


def _parse_list_page_html(list_page_html):
    """Parses the list html and returns the exported csv data.
    """
    # Conveniently, there's a csv export link. Grab it.
    EXPORT_LINK_REGEX = 'href=\"(/list/export.*)\"'
    export_link_match = re.search(EXPORT_LINK_REGEX, list_page_html)
    assert export_link_match, (
            "No export link found. Perhaps IMDB changed something?")
    export_link_sub_url = export_link_match.group(1)
    export_link_full_url = urlparse.urljoin(IMDB_URL_ROOT, export_link_sub_url)
    export_csv_data = urllib2.urlopen(export_link_full_url).read()
    return export_csv_data


def _get_movie_items_from_csv_data(csv_data):
    """Parses the data in the exported csv file and returns a list of
    adapted objects.
    """
    csv_fh = StringIO(csv_data)
    csv_reader = csv.DictReader(csv_fh)
    movie_list = [_adapt_exported_movie(movie) for movie in csv_reader]
    csv_fh.close()
    return movie_list


def _adapt_exported_movie(movie):
    return {
        LOCAL_KEY_URL: movie[IMDB_KEY_URL],
        LOCAL_KEY_TITLE: movie[IMDB_KEY_TITLE],
        LOCAL_KEY_YEAR: movie[IMDB_KEY_YEAR],
    }


if __name__ == '__main__':
    TEST_LIST_URL = 'http://www.imdb.com/list/-7NWd3EPpak/'
    print get_movie_items_from_list_url(TEST_LIST_URL)

    # # Test parsing.
    # with open('test_data/test_list_export.csv') as fh:
    #     print _get_movie_items_from_csv_data(fh.read())
