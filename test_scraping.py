from get_functions import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test file for functions in get_functions.py
'''

agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

test_list = [
    get_single_movie_reviews_info,
]


def test_get_single_movie_reviews_info():
    url = 'https://www.imdb.com/title/tt0111161/reviews'
    print(get_single_movie_reviews_info(url, agent_headers))


def test_get_single_movie_ratings_info():
    url = 'https://www.imdb.com/title/tt0111161/ratings'
    print(get_single_movie_ratings_info(url, agent_headers))


def test_get_single_movie_info():
    print('')
    # url = 'https://www.imdb.com/title/tt0111161/'
    url = 'https://www.imdb.com/title/tt0245429/'
    # print(get_single_movie_info(url, agent_headers,'Selenium'))
    print(get_single_movie_info(url, agent_headers))


def test_get_imdb_top250_links():
    print('')
    url = 'https://www.imdb.com/chart/top/'
    print(get_imdb_top250_links(url, agent_headers))


def test_get_imdb_top250_metadata():
    print('')
    url = 'https://www.imdb.com/chart/top/'
    links = get_imdb_top250_links(url, agent_headers)
    # print(get_imdb_top250_metadata(links, agent_headers,'Selenium'))
    print(get_imdb_top250_metadata(links, agent_headers))


def test_get_review_links():
    print('')
    url = 'https://www.imdb.com/title/tt0111161/reviews'
    get_review_links(url, agent_headers)


def test_get_single_review():
    print('')
    url = 'https://www.imdb.com/review/rw2081131/'
    print(get_single_review(url, agent_headers))


def test_get_all_reviews_of_single_movie():
    print('')
    url = 'https://imdb.com/title/tt0457430/reviews'
    print(get_all_reviews_of_single_movie(url, agent_headers))


def test_get_all_reviews_of_top250():
    print('')
    # m = 138
    # n = 239
    # print(get_imdb_top250_metadata(links, agent_headers,'Selenium'))
    metadata = pd.read_csv('test/imdb_top250_metadata.csv', header=0)
    # get_all_reviews_of_all_movies(metadata.iloc[m:n, :], agent_headers)
    get_all_reviews_of_all_movies(metadata.iloc[[239,249]],agent_headers)


def test_write_csv_file():
    print('')
    filename = 'test.csv'
    columns = ['a', 'b', 'c']
    records = [['1', 2, '3'], ['4', '5', '6']]
    print(write_csv_file(filename, columns, records))



pytest
