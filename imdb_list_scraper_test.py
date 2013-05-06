"""
Unit tests.
"""

import csv
from datetime import datetime
import unittest

from imdb_list_scraper import _get_movie_items_from_csv_data
from imdb_list_scraper import _parse_date
from imdb_list_scraper import LOCAL_KEY_CREATED
from imdb_list_scraper import LOCAL_KEY_MODIFIED
from imdb_list_scraper import LOCAL_KEY_TITLE
from imdb_list_scraper import LOCAL_KEY_URL
from imdb_list_scraper import LOCAL_KEY_YEAR


class TestImdbListScraper(unittest.TestCase):


    def test_parse_date(self):
        """Simple test for _parse_date.
        """
        IMDB_FORMAT_STRING = "Tue Oct 19 16:56:34 2010"
        result = _parse_date(IMDB_FORMAT_STRING)
        EXPECTED_RESULT = datetime(2010, 10, 19, 16, 56, 34)
        self.assertEqual(EXPECTED_RESULT, result)


    def test_get_movie_items_from_csv_data(self):
        """Simple test to make sure getting the list of movies works.
        """
        with open('test_data/test_list_export.csv') as fh:
            movie_items = _get_movie_items_from_csv_data(fh.read())

        # Just check the first movie to make sure this at least mostly works.
        first_movie = movie_items[0]
        self.assertEqual(datetime(2010, 10, 19, 16, 56, 34), first_movie[LOCAL_KEY_CREATED])
        self.assertEqual(datetime(2010, 10, 19, 16, 56, 34), first_movie[LOCAL_KEY_MODIFIED])
        self.assertEqual('Citizen Kane', first_movie[LOCAL_KEY_TITLE])
        self.assertEqual('http://www.imdb.com/title/tt0033467/', first_movie[LOCAL_KEY_URL])
        self.assertEqual('1941', first_movie[LOCAL_KEY_YEAR])


if __name__ == '__main__':
    unittest.main()
