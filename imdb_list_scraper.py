"""
Scrape data from an IMDB user's list.

In the current embodiment, we only support lists of movies.
"""

import csv
from datetime import datetime
import re
from StringIO import StringIO
import urllib2
import urlparse


IMDB_URL_ROOT = 'http://www.imdb.com/'

IMDB_KEY_CREATED = 'created'
IMDB_KEY_MODIFIED = 'modified'
IMDB_KEY_TITLE = 'Title'
IMDB_KEY_URL = 'URL'
IMDB_KEY_YEAR = 'Year'

LOCAL_KEY_CREATED = 'created'
LOCAL_KEY_MODIFIED = 'modified'
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
    """Reads the data in IMDB format and returns a list of python objects.
    """
    csv_fh = StringIO(csv_data)
    csv_reader = csv.DictReader(csv_fh)
    movie_list = [_adapt_exported_movie(movie) for movie in csv_reader]
    csv_fh.close()
    return movie_list


def _adapt_exported_movie(movie):
    """Adapts an IMDB movie object parsed from the csv file into a
    python object.
    """
    return {
        LOCAL_KEY_CREATED: _parse_date(movie[IMDB_KEY_CREATED]),
        LOCAL_KEY_MODIFIED: _parse_date(movie[IMDB_KEY_MODIFIED]),
        LOCAL_KEY_URL: movie[IMDB_KEY_URL],
        LOCAL_KEY_TITLE: movie[IMDB_KEY_TITLE],
        LOCAL_KEY_YEAR: movie[IMDB_KEY_YEAR],
    }


def _parse_date(imdb_date):
    """Parses the IMDB-formatted date, returning a python datetime object.

    At present, the IMDB format looks like:
        "Tue Oct 19 16:56:36 2010"
    """
    IMDB_FORMAT = '%a %b %d %H:%M:%S %Y'
    return datetime.strptime(imdb_date, IMDB_FORMAT)


if __name__ == '__main__':
    TEST_LIST_URL = 'http://www.imdb.com/list/-7NWd3EPpak/'
    print get_movie_items_from_list_url(TEST_LIST_URL)
