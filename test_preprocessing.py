from preprocessing import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test_data file for functions in get_functions.py
'''
default_df = pd.read_csv('test_data/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test_data/High and Low_reviews.csv', header=0)
agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}


def test_movie_duration_to_minutes():
    duration = '2 h 22 min'
    assert movie_duration_to_minutes(duration) == 142


def test_duration_converting():
    duration_converting()


def test_review_date_to_datetime():
    date = '1 January 2000'
    assert review_date_to_datetime(date) == '2000-01-01 00:00:00'


def test_date_converting():
    date_converting()


def test_preprocess_single_review():
    # test_review = ''
    preprocess_single_review()


def test_preprocess_all_reviews():
    preprocess_all_reviews()


def test_tokenization():
    a = tokenization(default_rw.review_title[0])
    b = stemming(a)


def test_get_docs_frequency():
    get_docs_frequency(default_rw.review_text)


def test_frequency_dataframe():
    print('')
    tf_idf = get_frequency_dataframe(default_rw.review_text)
    print(tf_idf.head())
    print(tf_idf.info())

pytest
